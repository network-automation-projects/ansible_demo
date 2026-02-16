from flask import Flask
import random

# Create a new Flask application where the home route displays an <h1> that says "Guess a number between 0 and 9" and display a gif of your choice from giphy.com.
# Alternatively use the one I found on Giphy: https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif
# Generate a random number between 0 and 9 or any range of numbers of your choice.
# Create a route that can detect the number entered by the user e.g "URL/3" or "URL/9" and checks that number against the generated random number. If the number is too low, tell the user it's too low, same with too high or if they found the correct number. try to make the <h1> text a different colour for each page.  e.g. If the random number was 5:
# 3 is too low:


app = Flask(__name__)

random_number = random.randint(0,9)
print(random_number)

@app.route('/')
def home():
    #show a gif
    return "<h1>Guess a number between 0 and 9</h1>" \
           "<img src='https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif'/>"


@app.route('/<int:num_guess>')
def guess(num_guess):
    if num_guess == random_number:
        return "<h1 style='color: green'>You found me!</h1>" \
               "<img src='https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif'/>"



if __name__ == "__main__":
    app.run(debug=True)