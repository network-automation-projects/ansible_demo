import turtle
import pandas
import random
from pathlib import Path


state_data = pandas.read_csv("50_states.csv")
all_states = state_data.state.tolist()
guessed = []

# Clear the tolearn.csv file for a fresh start
tolearn_path = Path("tolearn.csv")
if tolearn_path.exists():
    tolearn_path.unlink()

to_learn_list = [] #all_states

screen = turtle.Screen()
screen.title("US States Game")
image = "blank_states_img.gif"
screen.addshape(image)
turtle.shape(image) 

# def get_click_coord(x,y):
#     print(x,y)
# turtle.onscreenclick(get_click_coord)  #to grab coord. they clicked on



while len(guessed) < 50 :

    answer = screen.textinput(title = f"{len(guessed)} / 50 States Correct", prompt = "What's another state's name?")

    if answer is None or answer.lower() == "exit":
        break

    answer = answer.title()  # Convert to title case for matching


    if (answer in all_states) and (answer not in guessed):
        guessed.append(answer)
        ##to_learn_list.remove(answer) #remove that one, they know it
        
        
        
        
        state_data_row = state_data[state_data.state == answer]
        #create writer
        writer = turtle.Turtle()
        writer.penup() 
        writer.hideturtle()
        # writer.goto(state_data_row.x,state_data_row.y)  # this pulls the column including label
        writer.goto(state_data_row.x.item(),state_data_row.y.item())

        writer.write(answer)

Names = ["Emily", "David","Jessica","James","Ashley","Christopher","Amanda"]
Upper_Names = [name.upper() for name in Names if len(name) <=5]

student_scores = {Name:random.randint(1,100) for Name in Names}
#passed_students = [name for name in student_scores if student_scores >=70]
#print(passed_students)
#passed_students = {newkey: newvalue for (key,value) in dictionary if condition}
passed_students = {student:score for (student,score) in student_scores.items() if score >= 70}
print(passed_students)






to_learn_list = [state for state in all_states if state not in guessed]



#save states they haven't guessed to another csv
#start w list of all the states and delete the one's they guess as they go.  
# the list at the end is all the one's they need to learn
to_learn_df = pandas.DataFrame({'state': to_learn_list})
to_learn_df.to_csv("tolearn.csv", index = False)


#turtle.mainloop()    # OR screen.exitonclick()
screen.exitonclick()


""""old"""

    # if answer:
    #     answer = answer.upper()

    #     state_row = state_data[state_data.state == answer]
    #     if not state_row.empty:
    #         #get coord for that state
    #         x = int(state_row.x.iloc[0])
    #         y = int(state_row.y.iloc[0])

    #         writer.goto(x,y)
    #         writer.write(answer, align="center", font=("Arial", 8, "normal"))
