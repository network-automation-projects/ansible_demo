import requests
from bs4 import BeautifulSoup   #run pip install beautifulsoup4

URL = "https://web.archive.org/web/20200518073855/https://www.empireonline.com/movies/features/best-movies-2/"

# Write your code below this line 👇
#how do i know how to scrape the titles and rankings from the website?
#i can look at the website and see the titles and rankings.
#i can also look at the website and see the html code.
# i could print out the whole soup with 
#print(soup.prettify())

response = requests.get(URL)
web_page = response.text

soup = BeautifulSoup(web_page, "html.parser")
articles = soup.find_all("h3", class_="title")

print(articles)

#reverse the list of articles so the highest ranked movie is first.
#articles.reverse()
#or
articles = articles[::-1]

# article_texts = []
# article_links = []
# article_upvotes = []

#let's get rid of the )
for article in articles:
    print(article.getText())
    print(article.get("href"))

#let's get rid of the (1)
for article in articles:
    print(article.getText().replace("(", "").replace(")", ""))

#let's save the titles to a list and then write them to a file. movies.txt
movies = []
for article in articles:
    movies.append(article.getText().replace("(", "").replace(")", ""))

with open("movies.txt", "w") as file:
    for movie in movies:
        file.write(movie + "\n")

#let's read the file and print the titles.
with open("movies.txt", "r") as file:
    print(file.read())  