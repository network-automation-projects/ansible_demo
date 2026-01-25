"""pull from csv and learn pandas"""

# # import csv

# # with open("weather_data.csv") as w:
# #     data = csv.reader(w)
# #     temps = []
# #     for row in data:
# #         if row[1] != 'temp':
# #             temps.append(int(row[1]))
            
# #     print (temps)

# """enter pandas for python data analysis"""
import pandas

# data = pandas.read_csv("weather_data.csv")
# #print(data["temp"])

# temp_list = data["temp"].to_list()
# #print(temp_list)

# num_total = 0
# for num in temp_list:
#     num_total = num_total + num

# #print (int(num_total / len(temp_list)))

# #OR

# #print (data["temp"].mean())

# #get max
# #print (data["temp"].max())

# #print (data["condition"])
# #print (data.condition)
# #(same because it makes them into attributes behind the scenes)

# #rows
# #print(data[data.day == 'Monday']) #pull the row for Monday

# #pull row w max temp
# #print(data[data.temp == int(data['temp'].max())]   )

# #temp on Monday in F
# tempf = 0
# tempMonday = data[data.day == "Monday"].temp

# #print( ( tempMonday * 9/5) + 32 )

# #make panda Dataframe from scratch

# #grab or type out a dictionary and make it into a dataframe
# temp_dict = data.to_dict()

# # new_dataframe = pandas.DataFrame(temp_dict)

# # print(new_dataframe)

# # new_dataframe.to_csv("new-file.csv")


#""" squirrel census data manipulation """

sq_data = pandas.read_csv("sq_data.csv") 

num_of_squirrels = 0

#grab each row and see which color it is ?

# grouped = sq_data.groupby("Primary Fur Color")

# result = grouped.count()

# print (result)

# better_result = grouped["Primary Fur Color"].count()

# print (better_result)

#OR

#get them one type at a time

#get all the gray squirrels
gray_squirrels = len(sq_data[sq_data["Primary Fur Color"] == "Gray"])

print (gray_squirrels)
