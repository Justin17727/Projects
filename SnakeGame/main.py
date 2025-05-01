import tkinter as tk
import random


def update(snake_coordinates: list[list[int]], x_direction: int, y_direction: int) -> None:
    # use it to update the snake coordinates
    count = 0
    global a, b
    apple_loc.append(snake_coordinates[-1])
    if x_direction == 1 and y_direction == 0:
        for coordinates in snake_coordinates:
            if count == 0:
                count += 1
                a = coordinates[0]
                b = coordinates[1]
                coordinates[1] += 1
                continue
            coordinates[0], a = a, coordinates[0]
            coordinates[1], b = b, coordinates[1]
    if x_direction == -1 and y_direction == 0:
        for coordinates in snake_coordinates:
            if count == 0:
                count += 1
                a = coordinates[0]
                b = coordinates[1]
                coordinates[1] -= 1
                continue
            coordinates[0], a = a, coordinates[0]
            coordinates[1], b = b, coordinates[1]
    if x_direction == 0 and y_direction == 1:
        for coordinates in snake_coordinates:
            if count == 0:
                count += 1
                a = coordinates[0]
                b = coordinates[1]
                coordinates[0] -= 1
                continue
            coordinates[0], a = a, coordinates[0]
            coordinates[1], b = b, coordinates[1]
    if x_direction == 0 and y_direction == -1:
        for coordinates in snake_coordinates:
            if count == 0:
                count += 1
                a = coordinates[0]
                b = coordinates[1]
                coordinates[0] += 1
                continue
            coordinates[0], a = a, coordinates[0]
            coordinates[1], b = b, coordinates[1]


def on_key_press(event) -> bool:
    # use it to set directions
    global x, y
    if event.keysym == 'Up' and y != -1:
        x, y = 0, 1
        return True
    if event.keysym == 'Down' and y != 1:
        x, y = 0, -1
        return True
    if event.keysym == 'Right' and x != -1:
        x, y = 1, 0
        return True
    if event.keysym == 'Left' and x != 1:
        x, y = -1, 0
        return True
    return False


def paint(snake_coordinates: list[list[int]]):
    # place the snake coordinates on screen
    k = 0
    for coord in snake_coordinates:
        snake[k].grid(row=coord[0], column=coord[1], sticky='nswe')
        k += 1


def collision(snake_coordinates: list[list[int]]) -> bool:
    # collision with walls
    for coord in snake_coordinates:
        if coord[0] < 0:
            return True
        elif coord[0] >= 50:
            return True
        elif coord[1] < 0:
            return True
        elif coord[1] >= 50:
            return True
    return False


def search(snake_coordinates: list[list[int]], item: list[int]) -> bool:
    # search the item excluding the first
    s = 0
    for coord in snake_coordinates:
        if s == 0:
            s += 1
            continue
        if coord == item:
            return True
        s += 1
    return False


def snake_collision(snake_coordinates: list[list[int]]) -> bool:
    # collision with snake itself
    pixel: list[int] = snake_coordinates[0]
    if search(snake_coordinates, pixel):
        return True
    return False


def place_apple() -> list[int]:
    # place an apple on window
    index = random.choice([place for place in apple_loc if place not in snek])
    apple.grid(row=index[1], column=index[0], sticky='nswe')
    return [index[1], index[0]]


def snake_growth(snake_coordinates: list[list[int]], snake_frame: list[tk.Frame]):
    # grow snake longer by 1 block
    global apple_loc
    new: tk.Frame = tk.Frame(panel,  width=1, height=1, bg='green')
    snake_frame.append(new)
    if x != 0:
        if x == 1:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x, loc_y + 1])
        else:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x, loc_y - 1])
    else:
        if y == 1:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x + 1, loc_y])
        else:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x - 1, loc_y])


def score_display():
    # display score
    global score, score_card
    score += 1
    score_card.config(text=f'Score: {score}')
    pass


def apple_logic(snake_coordinates: list[list[int]], apple_coordinates: list[list[int]]) -> None:
    # check if apple is eaten and then respawn an apple
    global loc, score
    if apple_coordinates[0] == snake_coordinates[0]:
        score_display()
        loc.clear()
        loc.append(place_apple())
        snake_growth(snake_coordinates, snake)


def work(window: tk.Frame) -> None:
    # time scheduled updates
    try:
        update(snek, x, y)
        apple_logic(snek, loc)
        paint(snek)
        if collision(snek) or snake_collision(snek):
            root.destroy()
        window.after(120, work, window)
    except Exception as e:
        print(e)
        root.destroy()


x: int = 0
y: int = 1
a: int = 25
b: int = 25
score: int = 0
root: tk.Tk = tk.Tk()
snake: list[tk.Frame] = []
snek: list[list[int]] = []
panel: tk.Frame = tk.Frame(root, width=500, height=500, bg='#fff2cc')
apple: tk.Frame = tk.Frame(panel, width=10, height=10, bg='red')
apple_loc: list[list[int]] = []
for element1 in range(50):
    for element2 in range(50):
        apple_loc.append([element1, element2])
score_card: tk.Label = tk.Label(root, text=f'Score: {score}')
for i in range(50):
    for j in range(50):
        apple_loc.append([i, j])
loc: list[list[int]] = []
for m in range(25):
    snake.append(tk.Frame(panel, width=10, height=10, bg='green'))
    snek.append([a + m, b])
    apple_loc.remove([a + m, b])
root.geometry('500x550')
for i in range(0, 50):
    panel.grid_rowconfigure(i, minsize=10)
    panel.grid_columnconfigure(i, minsize=10)
for m in range(25):
    snake[m].grid(row=a + m, column=b)
root.bind('<KeyPress>', on_key_press)
root.title('Snake Game')
root.resizable(False, False)
panel.pack(pady=20, expand=True, fill='x')
loc.append(place_apple())
score_card.place(x=225, y=0)
root.after(120, work, root)
root.mainloop()
