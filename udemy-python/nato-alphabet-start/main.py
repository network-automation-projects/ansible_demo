import pandas
data = pandas.read_csv("nato_phonetic_alphabet.csv")


phonetic_dict = {row.code: row.letter for (index, row) in data.iterrows()}

print ("***") 
print(phonetic_dict)

def game_go():
    word = input ("Type Word: ").upper()

    # try:
    letter_codes = [phonetic_dict[i] for i in word]
    print(letter_codes)
    # except KeyError:
    #     print("Choose a real letter.")
    #     game_go()
    # else:
    #     print(letter_codes)

game_go()



# student_dict = {
#     "student": ["Angela", "James", "Lily"], 
#     "score": [56, 76, 98]
# }

# #Looping through dictionaries:
# for (key, value) in student_dict.items() if letter in letters:
#     #Access key and value
#     pass

from os import name
import pandas
# student_data_frame = pandas.DataFrame(student_dict)

# #Loop through rows of a data frame
# for (index, row) in student_data_frame.iterrows():
#     #Access index and row
#     #Access row.student or row.score
#     pass

# Keyword Method with iterrows()
# {new_key:new_value for (index, row) in df.iterrows()}

#TODO 1. Create a dictionary in this format:
{"A": "Alfa", "B": "Bravo"}

#loading data
data = pandas.read_csv("nato_phonetic_alphabet.csv")
natoDict = {code: letter for (code,letter) in data.iterrows()}
print ("999")
print(natoDict)



#TODO 2. Create a list of the phonetic code words from a word that the user inputs.
word = input("Please input a word to convert to nato alphabet\n")
   
letters =  list[str](word) #word
print(letters)
#for each of the letters in word, function will find the letter which matches then append the 
nameList = []
#for (index,row) in data

for letter in letters:
    
    #print(f"letter is {letter}")
    #loop through dataframe to find the nato answer
    for (index, row) in data.iterrows():
        #is this a row with out letter in it?
        #print(row.letter)
        #print("this code block is running")
        if letter.upper() == row.letter:
            print("conditional is functional")
            nameList.append(row.code)

        found = True

#print(nameList)


# for (natoDict.code, natoDict.letter) in natoDict.items():
#     if letter in letters:      #letter is one we want then add to list
#         print(letter + " " + natoLetter)
#         nameList.append(natoLetter)

if found == False:
    raise ValueError("Letter not found")

print(nameList)
# wordInNato = [natoDict.code for letter in letters if letter in natoDict.items() ]
# print(wordInNato)
