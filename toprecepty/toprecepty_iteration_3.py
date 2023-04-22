from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame
import csv

url = "https://www.toprecepty.cz/vsechny_recepty.php"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

articles = soup.find_all("article", {"class": "b-recipe"})

recipe_list = []
for article in articles:
    recipe_name = article.find("a", {"class": "b-recipe__link link-mask"}).get_text().strip()
    recipe_link = "https://www.toprecepty.cz" + article.find("a", {"class": "b-recipe__link link-mask"})["href"]
    recipe_image = article.find("img", {"class": "img__img"})["src"]

    recipe_dict = {
        "recipe_source_id": recipe_link.split("/")[4].split("-")[0],
        "recipe_name": recipe_name,
        "recipe_link": recipe_link,
        "recipe_image": recipe_image
    }

    recipe_list.append(recipe_dict)

## comment this line to make it run for all recipes on the page
#recipe_list = [recipe_list[7]]
recipe_list_2 = []
i = 1
for recipe in recipe_list:
    print(recipe)
    recipe_detail_html = urlopen(recipe["recipe_link"]).read()
    recipe_detail_soup = BeautifulSoup(recipe_detail_html, features="html.parser")
    
    recipe["id"] = i
    recipe["recipe_stars"] = recipe_detail_soup.find("span", {"class": "stars__rating"}).get_text().strip()
    recipe["recipe_rating_cnt"] = recipe_detail_soup.find("span", {"class": "stars__count"}).get_text().strip()
    recipe["recipe_author"] = recipe_detail_soup.find_all("a", {"class": "author__link author__link--name link-mask"})[2].get_text().strip()
    #recipe["recipe_time"] = recipe_detail_soup.find("p", {"class": "b-recipe-info__info item-icon u-print"}).get_text().strip().replace('\n', '.').replace('\t', '.').replace('\xa0', ' ')
    recipe["recipe_created"] = recipe_detail_soup.find("p", {"class": "b-recipe-info__info item-icon"}).get_text().strip()
    recipe["recipe_comment_cnt"] = recipe_detail_soup.find("a", {"class": "b-recipe-info__link item-icon"}).get_text().strip()

    recipe_time = recipe_detail_soup.find("p", {"class": "b-recipe-info__info item-icon u-print"})
    if (recipe_time is not None):
                recipe["recipe_time"] = recipe_time.get_text()

    ingredients = recipe_detail_soup.find("div", {"class": "b-parameters b-parameters--ingredients u-mb-sm b-highlight u-last-m0"})

    ingredient_dict = {}
    ingredient_dict["recipe_id"] = i

    serve_cnt = ingredients.find("span", {"class": "b-parameters__amount"})
    if (serve_cnt is not None):
                recipe["serve_cnt"] = serve_cnt.get_text()

    serve_unit = ingredients.find("span", {"data-portions-target": "unit"})
    if (serve_unit is not None):
        recipe["serve_unit"] = serve_unit.get_text()

    recipe_sections = recipe_detail_soup.find_all(lambda tag: tag.name == 'label' and tag.get('class') == ['b-parameters__label'])

    sections = ["Suroviny"]
    for section in recipe_sections:
        section_name = section.find("b").get_text().strip().replace(":", "")
        sections.append(section_name)

    recipe["sections"] = sections
    recipe_list_2.append(recipe)

    #ingredient_nutrition_url = "https://www.toprecepty.cz" + recipe_detail_soup.find("a", {"class": "b-parameters__btn b-parameters__btn--modal btn btn--block"})["href"]
    ingredient_nutrition_url = "https://www.toprecepty.cz/nutricni-hodnoty/" + recipe["recipe_source_id"]
    ingredient_nutrition_html = urlopen(ingredient_nutrition_url).read()
    ingredient_nutrition_soup = BeautifulSoup(ingredient_nutrition_html, features="html.parser")

    recipe["ingredient_nutrition_url"] = ingredient_nutrition_url
    print(recipe)

    grid = ingredient_nutrition_soup.find_all("table")

    nutrition_table_html = grid[0]
    ingredient_table_html = grid[1]

    ingredient_rows = ingredient_table_html.find_all("tr")
    ingredient_rows.pop(0)
    
    print(sections)
    ingredient_list = []
    empty_table_rows = 0
    for row in ingredient_rows:
        ingredient = {}
        ingredient["recipe_id"] = recipe["id"]
        #ingredient["section"] = recipe["sections"][empty_table_rows]
        ingredient["name"] = row.find("td", {"class": None}).get_text()
        ingredient["description"] = row.find("th").get_text().strip().split("\n")
        ingredient["amount"] = row.find("span").get_text()
        #print(empty_table_rows)
        if ingredient["name"] == "":
            empty_table_rows = empty_table_rows + 1
            #ingredient["section"] = recipe["sections"][empty_table_rows]
        ingredient_list.append(ingredient)

    nutrition_rows = nutrition_table_html.find_all("tr")    
    
    nutrition_list = []
    for row in nutrition_rows:
        nutrition = {}
        nutrition["recipe_id"] = recipe["id"]
        nutrition["name"] = row.find("td").get_text()
        nutrition["value"] = row.find("span").get_text()
        nutrition["unit"] = row.find("th").get_text()
        nutrition_list.append(nutrition)
    
    recipe = {}
    sections = []
    empty_table_rows = 0

recipe_df = DataFrame(recipe_list_2)
ingredient_df = DataFrame(ingredient_list)
nutrition_df = DataFrame(nutrition_list)
recipe_df.to_csv("recipe.csv", sep=',', encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
ingredient_df.to_csv("ingredient.csv", sep=',', encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
nutrition_df.to_csv("nutrition.csv", sep=',', encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)

#print(recipe_df)
#print(ingredient_df)
#print(nutrition_df)