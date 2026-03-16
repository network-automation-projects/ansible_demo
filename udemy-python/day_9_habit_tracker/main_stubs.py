# Create a Python program that lets a user track habits over time (exercise, reading, etc.).

import requests

habits = {
    "eating healthy": [],
    "exercise": [],
    "coding": []
}


# Create a function that allows the user to add a new habit to the dictionary.

def add_habit(habit_name):
    # check if habit already exists

    # if not, add it to dictionary
    pass


# Create a function that records when a habit is completed today.

def record_habit(habit_name, value):
    # check if habit exists

    # append the value to the list

    pass
    

# Create a function that calculates totals and averages.

def show_stats(habit_name):

    # get list of values

    # calculate total

    # calculate average

    # print results

    pass

# Create a loop so the program keeps running until the user exits.

running = True

while running:

    print("Habit Tracker")
    print("1. Add habit")
    print("2. Record habit")
    print("3. Show stats")
    print("4. Exit")

    choice = input("Choose option: ")

    if choice == "1":
        # call add_habit()

    elif choice == "2":
        # call record_habit()

    elif choice == "3":
        # call show_stats()

    elif choice == "4":
        running = False


# Save the dictionary to a file so data persists.

import json

def save_data():
    with open("habits.json", "w") as file:
        json.dump(habits, file)

def load_data():
    global habits
    try:
        with open("habits.json", "r") as file:
            habits = json.load(file)
    except FileNotFoundError:
        habits = {}


# Instead of local storage, send habit data to an API.
# POST /habits
# POST /habit-completion
# GET /habit-stats

# Once everything works, try adding:
# streak tracking
# habit deletion
# calendar view
# weekly summaries