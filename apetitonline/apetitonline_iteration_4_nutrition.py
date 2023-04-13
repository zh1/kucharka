# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

with open("article_details_1.html", "r", encoding='utf-8') as article_detail_example:
    detail_example = article_detail_example.read()

soup = BeautifulSoup(detail_example, features="html.parser")

nutritions = soup.find_all("div", {"class": "s-recipe-header__nutritional"})

nutrition_list = []
for nutrition in nutritions:
    nutrition_item_list = nutrition.find_all("div", {"class": "s-recipe-header__nutritional-item"})

    for item in nutrition_item_list:
        nutrition_item = item.find("span").get_text()
        nutrition_amount = item.find("span").findNext("span").get_text()
        nutrition_unit = nutrition_amount.split(" ", 1)[1]
        nutrition_amount = nutrition_amount.split(" ", 1)[0]

        print(nutrition_item, nutrition_amount, nutrition_unit)
