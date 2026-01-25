from bs4 import BeautifulSoup 

with open("website.html") as website_file:
    data = website_file.read()

    soup = BeautifulSoup(data, "html.parser")

