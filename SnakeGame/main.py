import tkinter as tk
import random


def start_over() -> None:
    # reinitialise everything for restarting the game
    global x, y, status_flag, game_over_flag, snake_head_x_pos, snake_head_y_pos
    global score, root, snake, snek, panel, apple, apple_loc, score_card, loc, game_over_text
    x = 0
    y = 1
    status_flag = False
    game_over_flag = False
    snake_head_y_pos = 25
    snake_head_x_pos = 25
    score = 0
    for pix in snake:
        pix.destroy()
    snake.clear()
    for text in game_over_text:
        text.destroy()
    game_over_text.clear()
    snek.clear()
    apple_loc.clear()
    for e1 in range(50):
        for e2 in range(50):
            apple_loc.append([e1, e2])
    score_card.config(text=f'Score: {score}')
    loc.clear()
    for s in range(25):
        snake.append(tk.Frame(panel, width=10, height=10, bg='green'))
        snek.append([snake_head_y_pos + s, snake_head_x_pos])
        apple_loc.remove([snake_head_y_pos + s, snake_head_x_pos])
    for s in range(0, 50):
        panel.grid_rowconfigure(s, minsize=10)
        panel.grid_columnconfigure(s, minsize=10)
    for s in range(25):
        snake[s].grid(row=snake_head_y_pos + s, column=snake_head_x_pos)
    loc.append(place_apple())


def update(x_direction: int, y_direction: int) -> None:
    # use it to update the snake coordinates
    count = 0
    global snake_head_y_pos, snake_head_x_pos, snek
    apple_loc.append(snek[-1])
    if x_direction == 1 and y_direction == 0:
        for coordinates in snek:
            if count == 0:
                count += 1
                snake_head_y_pos = coordinates[0]
                snake_head_x_pos = coordinates[1]
                coordinates[1] += 1
                continue
            coordinates[0], snake_head_y_pos = snake_head_y_pos, coordinates[0]
            coordinates[1], snake_head_x_pos = snake_head_x_pos, coordinates[1]
    if x_direction == -1 and y_direction == 0:
        for coordinates in snek:
            if count == 0:
                count += 1
                snake_head_y_pos = coordinates[0]
                snake_head_x_pos = coordinates[1]
                coordinates[1] -= 1
                continue
            coordinates[0], snake_head_y_pos = snake_head_y_pos, coordinates[0]
            coordinates[1], snake_head_x_pos = snake_head_x_pos, coordinates[1]
    if x_direction == 0 and y_direction == 1:
        for coordinates in snek:
            if count == 0:
                count += 1
                snake_head_y_pos = coordinates[0]
                snake_head_x_pos = coordinates[1]
                coordinates[0] -= 1
                continue
            coordinates[0], snake_head_y_pos = snake_head_y_pos, coordinates[0]
            coordinates[1], snake_head_x_pos = snake_head_x_pos, coordinates[1]
    if x_direction == 0 and y_direction == -1:
        for coordinates in snek:
            if count == 0:
                count += 1
                snake_head_y_pos = coordinates[0]
                snake_head_x_pos = coordinates[1]
                coordinates[0] += 1
                continue
            coordinates[0], snake_head_y_pos = snake_head_y_pos, coordinates[0]
            coordinates[1], snake_head_x_pos = snake_head_x_pos, coordinates[1]


def on_key_press(event) -> bool:
    # use it to set directions or restart game
    global x, y, status_flag, game_over_flag
    if not status_flag:
        status_flag = True
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
        elif game_over_flag and event.keysym == 'Return':
            start_over()
            game_over_flag = False
            root.after(120, work, root)
        else:
            return False
    else:
        return False


def paint(snake_coordinates: list[list[int]]) -> None:
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
    available: list[list[int]] = [place for place in apple_loc if place not in snek]
    index = random.choice(available)
    apple.grid(row=index[0], column=index[1], sticky='nswe')
    return [index[0], index[1]]


def snake_growth(snake_coordinates: list[list[int]], snake_frame: list[tk.Frame]) -> None:
    # grow snake longer by 1 block
    global apple_loc
    new: tk.Frame = tk.Frame(panel,  width=1, height=1, bg='green')
    snake_frame.append(new)
    pix1: list[int] = snake_coordinates[-1]
    pix2: list[int] = snake_coordinates[-2]
    if pix1[0] == pix2[0]:
        if pix1[1] > pix2[1]:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x, loc_y + 1])
        else:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x, loc_y - 1])
    else:
        if pix1[0] > pix2[0]:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x + 1, loc_y])
        else:
            loc_x, loc_y = snake_coordinates[-1]
            snake_coordinates.append([loc_x - 1, loc_y])


def score_display() -> None:
    # display score
    global score, score_card
    score += 1
    score_card.config(text=f'Score: {score}')
    return


def apple_logic(snake_coordinates: list[list[int]], apple_coordinates: list[list[int]]) -> None:
    # check if apple is eaten and then respawn an apple
    global loc, score
    if apple_coordinates[0] == snake_coordinates[0]:
        score_display()
        loc.clear()
        loc.append(place_apple())
        snake_growth(snake_coordinates, snake)


def game_over() -> None:
    # to showcase game over screen
    global game_over_flag, game_over_text
    game_over_flag = True
    game_over_text.append(tk.Label(panel, text='Game Over!', font=('Arial', 10)))
    game_over_text[0].place(x=215, y=225)


def work(window: tk.Frame) -> None:
    # time scheduled updates
    global status_flag
    try:
        update(x, y)
        status_flag = False
        apple_logic(snek, loc)
        if collision(snek) or snake_collision(snek):
            game_over()
            status_flag = False
            return
        paint(snek)
        window.after(120, work, window)
    except Exception as e:
        print(e)
        root.destroy()


x: int = 0
y: int = 1
status_flag: bool = False  # highlighting whether the user has changed direction of snake/ for buffered event handling
game_over_flag: bool = False  # highlighting whether game has ended
snake_head_y_pos: int = 25  # highlighting row for snake head
snake_head_x_pos: int = 25  # highlighting column for snake head
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
loc: list[list[int]] = []
for m in range(25):
    snake.append(tk.Frame(panel, width=10, height=10, bg='green'))
    snek.append([snake_head_y_pos + m, snake_head_x_pos])
    apple_loc.remove([snake_head_y_pos + m, snake_head_x_pos])
root.geometry('500x550')
for i in range(0, 50):
    panel.grid_rowconfigure(i, minsize=10)
    panel.grid_columnconfigure(i, minsize=10)
for m in range(25):
    snake[m].grid(row=snake_head_y_pos + m, column=snake_head_x_pos)
game_over_text: list[tk.Label] = []
root.bind('<KeyPress>', on_key_press)
root.title('Snake Game')
root.resizable(False, False)
panel.pack(pady=20, expand=True, fill='x')
loc.append(place_apple())
score_card.place(x=225, y=0)
root.after(120, work, root)
root.mainloop()
