import tkinter as tk
import random

GAME_WIDTH = 600
GAME_HEIGHT = 400
SPEED = 100       # Smaller is faster
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BG_COLOR = "#1A1A1A"

class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

class Food:
    def __init__(self, canvas, snake):
        self.coordinates = []
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) -1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) -1) * SPACE_SIZE
            if [x, y] not in snake.coordinates:
                break
        self.coordinates = [x, y]
        self.food = canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )

def next_turn(snake, food):
    global game_running

    if not game_running:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food.__init__(canvas, snake)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Game over conditions
    if (
        x < 0 or x >= GAME_WIDTH
        or y < 0 or y >= GAME_HEIGHT
        or [x, y] in snake.coordinates[1:]
    ):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    if not game_running:
        return
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def game_over():
    global game_running
    game_running = False
    canvas.create_text(
        GAME_WIDTH/2, GAME_HEIGHT/2-30, font=("Arial", 32, "bold"), fill="#FFFFFF",
        text="GAME OVER"
    )
    canvas.create_text(
        GAME_WIDTH/2, GAME_HEIGHT/2+10, font=("Arial", 20), fill="#FF8888",
        text="Final Score: {}".format(score)
    )
    restart_button.pack(pady=10)

def start_game():
    global score, direction, snake, food, game_running

    start_button.pack_forget()
    restart_button.pack_forget()

    score = 0
    direction = "right"
    game_running = True
    label.config(text="Score:0")
    canvas.delete(tk.ALL)

    snake = Snake()
    food = Food(canvas, snake)

    for x, y in snake.coordinates:
        square = canvas.create_rectangle(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
        )
        snake.squares.append(square)

    next_turn(snake, food)

window = tk.Tk()
window.title("Snake Game by Perplexity AI")
window.resizable(False, False)

score = 0
direction = "right"
game_running = False

label = tk.Label(window, text="Score:0", font=("Arial", 24), bg=BG_COLOR, fg="#FFF")
label.pack(fill="x")

canvas = tk.Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

start_button = tk.Button(window, text="Start Game", font=("Arial", 16), command=start_game)
start_button.pack(pady=10)

restart_button = tk.Button(window, text="Restart Game", font=("Arial", 16), command=start_game)
# Initially hidden
restart_button.pack_forget()

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.mainloop()
