from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.toprecepty.cz/vsechny_recepty.php"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

with open("first_page_toprecepty.html", "w", encoding='utf-8') as first_page_file:
    first_page_file.write(str(soup.prettify()))

articles = soup.find_all("article", {"class": "b-recipe"})

with open("articles.html", "w", encoding='utf-8') as articles_file:
    articles_file.write(str(articles))

print(len(articles))