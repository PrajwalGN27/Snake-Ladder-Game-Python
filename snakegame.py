#                                     Snake Game

from tkinter import *
import random

Game_Width = 700
Game_Height = 540
Speed = 100
Space_Size = 20
Body_Parts = 3
Snake_Color = "#00FF60"
Food_Color = "#FF2A00"
Background_Color = "#000020"

class Snake:
    def __init__(self):
        self.body_size = Body_Parts
        self.coordinates = []
        self.squares = []

        for i in range(0, Body_Parts):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + Space_Size, y + Space_Size, fill=Snake_Color, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (Game_Width // Space_Size) - 1) * Space_Size
        y = random.randint(0, (Game_Height // Space_Size) - 1) * Space_Size
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + Space_Size, y + Space_Size, fill=Food_Color, tag="food")

def next_turn(snake, food):
    x, y = snake.coordinates[0]

    if direction == "up":
        y -= Space_Size
    elif direction == "down":
        y += Space_Size
    elif direction == "left":
        x -= Space_Size
    elif direction == "right":
        x += Space_Size

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(x, y, x + Space_Size, y + Space_Size, fill=Snake_Color)
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(Speed, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= Game_Width:
        return True
    elif y < 0 or y >= Game_Height:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2,
                       canvas.winfo_height()/2,
                       font=('consolas', 70),
                       text="GAME OVER",
                       fill="red",
                       tag="gameover")

# ---------------- MAIN ---------------- 
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = Label(window, text="Score: {}".format(score), font=('consolas', 40))
label.pack()

canvas = Canvas(window, bg=Background_Color, height=Game_Height, width=Game_Width)
canvas.pack()

window.update()

window_width = window.winfo_width()
window_height = window.winfo_height()
screen_height = window.winfo_screenheight()
screen_width = window.winfo_screenwidth()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)
window.mainloop()