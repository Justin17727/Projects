import tkinter as tk


def update(snake_coordinates: list[list[int]], x_direction: int, y_direction: int) -> None:
    # use it to update the snake coordinates
    count = 0
    global a, b
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
    if event.keysym == 'Up':
        x = 0
        y = 1
        return True
    if event.keysym == 'Down':
        x = 0
        y = -1
        return True
    if event.keysym == 'Right':
        x = 1
        y = 0
        return True
    if event.keysym == 'Left':
        x = -1
        y = 0
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


def work(window: tk.Frame):
    # time scheduled updates
    try:
        update(snek, x, y)
        paint(snek)
        if collision(snek):
            root.destroy()
        window.after(120, work, window)
    except Exception as e:
        root.destroy()


'''def start():
    # start the timer here for regular update and direction setting
    # try:
    while True:
        update(snek, x, y)
        paint(snek)
        time.sleep(1/10)
    except Exception as e:
        print(e)
        root.destroy()
    pass

'''
x = 0
y = 1
a = 25
b = 25
root = tk.Tk()
snake: list[tk.Frame] = []
snek: list[list[int]] = []
for m in range(25):
    snake.append(tk.Frame(root, width=1, height=1, bg='green'))
    snek.append([a + m, b])
root.geometry('500x500')
for i in range(0, 50):
    root.grid_rowconfigure(i, weight=10, pad=0)
    root.grid_columnconfigure(i, weight=10, pad=0)
for m in range(25):
    snake[m].grid(row=a + m, column=b)
root.bind('<KeyPress>', on_key_press)
root.title('Snake Game')
root.maxsize(height=500, width=500)
root.after(120, work, root)
root.mainloop()
