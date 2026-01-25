from turtle import Turtle
ALIGNMENT = "center"
FONT = ("Courier", 24, "normal")

with open("data.txt") as data:
    high_score = int(data.read())

class Scoreboard(Turtle):

    def __init__(self):
        super().__init__()
        self.score = high_score
        self.color("white")
        self.penup()
        self.goto(0, 270)
        self.hideturtle()
        self.update_scoreboard()

    def update_scoreboard(self):
        self.write(f"Score: {self.score}", align=ALIGNMENT, font=FONT)

    def game_over(self):
        self.goto(0, 0)
        self.write("GAME OVER", align=ALIGNMENT, font=FONT)

    def increase_score(self):
        self.score += 1
        self.clear()
        self.update_scoreboard()
