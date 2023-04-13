# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.apetitonline.cz/recepty"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

articles = soup.find_all("article", {"class": "a-teaser content_recipe"})

for article in articles:
    receipt_name = article.find("div", {"class": "a-teaser__content"}).find("span").get_text()
    receipt_link = article.find("a", {"class": "a-teaser__link"})["href"]
    receipt_image = article.find("img")["src"]

    #receipt_difficulty = article.find("i", {"class": "icon-difficulty-1"}).get_text()
    receipt_rating = article.find("div", {"class": "e-rating"})["data-rating-average"]
    receipt_stars = article.find("div", {"class": "e-rating"})["data-stars"]

    receipt_data_items = article.find_all("span", {"class": "a-teaser__data-item"})
    for receipt_data in receipt_data_items:
        if ("icon-stopwatch" in str(receipt_data)):
            receipt_time = receipt_data.get_text()
        if ("icon-difficulty" in str(receipt_data)):
            receipt_difficulty = receipt_data.get_text()

    print(receipt_name, receipt_link, receipt_rating, receipt_stars, receipt_image, receipt_time, receipt_difficulty)