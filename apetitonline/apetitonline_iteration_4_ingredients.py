# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

with open("article_details_1.html", "r", encoding='utf-8') as article_detail_example:
    detail_example = article_detail_example.read()

soup = BeautifulSoup(detail_example, features="html.parser")

ingredients = soup.find_all("div", {"class": "s-recipe__ingredients"})

#with open("ingredients_1.html", "w", encoding='utf-8') as ingredients_1_example:
#    ingredients_1_example.write(str(ingredients))
#
#with open("process_1.html", "w", encoding='utf-8') as process_1_example:
#    process_1_example.write(str(processes))

ingredients_list = []
for ingredient in ingredients:
    ingredient_item_list = ingredient.find_all("div", {"class": "s-recipe__ingredients-item"})

    for item in ingredient_item_list:
        ingredient_name = item.find("strong", {"class": "s-recipe__ingredients-name"})
        ingredient_name_link = item.find("strong", {"class": "s-recipe__ingredients-name link--primary"})
        if (ingredient_name is not None):
            ingredient_name = ingredient_name.get_text()
        elif (ingredient_name_link is not None):
            ingredient_name = ingredient_name_link.get_text()

        ingredient_description = item.find("div", {"class": "s-recipe__ingredients-description"})
        if (ingredient_description is not None):
            ingredient_description = ingredient_description.get_text()

        ingredient_quantity = item.find("span", {"class": "s-recipe__ingredients-quantity"})
        if (ingredient_quantity is not None):
            ingredient_quantity = ingredient_quantity.get_text()

        ingredient_unit = item.find("span", {"class": "s-recipe__ingredients-unit"})
        if (ingredient_unit is not None):
            ingredient_unit = ingredient_unit.get_text()

        ingredient_subtitle = item.find_previous("div", class_="s-recipe__ingredients-subtitle")
        if (ingredient_subtitle is not None):
            ingredient_subtitle = ingredient_subtitle.get_text()
        else:
            ingredient_subtitle = "Suroviny"

        if (ingredient_name is not None):
            print(ingredient_subtitle, ingredient_name, ingredient_description, ingredient_quantity, ingredient_unit)