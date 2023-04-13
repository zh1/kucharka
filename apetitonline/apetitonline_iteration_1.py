# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.apetitonline.cz/recepty"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

#with open("first_page.html", "w", encoding='utf-8') as first_page_file:
#    first_page_file.write(str(soup.prettify()))
## Prints html source of a page in readable format
#print(soup.prettify())

articles = soup.find_all("article", {"class": "a-teaser content_recipe"})

with open("articles.html", "w", encoding='utf-8') as articles_file:
    articles_file.write(str(articles))

print(len(articles))