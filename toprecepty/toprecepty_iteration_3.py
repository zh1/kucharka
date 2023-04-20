from urllib.request import urlopen
from bs4 import BeautifulSoup

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
        "recipe_name": recipe_name,
        "recipe_link": recipe_link,
        "recipe_image": recipe_image,
        #"recipe_rating": recipe_rating,
        #"recipe_stars": recipe_stars,
        #"recipe_author": recipe_author,
        #"recipe_time": recipe_time,
        #"recipe_test": recipe_test
    }

    recipe_list.append(recipe_dict)

recipe_list = [recipe_list[7]]
i = 1
for recipe in recipe_list:

    recipe_detail_html = urlopen('https://www.toprecepty.cz/recept/74039-ryzovy-nakyp-z-remosky/').read()
    recipe_detail_soup = BeautifulSoup(recipe_detail_html, features="html.parser")
    
    recipe["id"] = i
    recipe["recipe_stars"] = recipe_detail_soup.find("span", {"class": "stars__rating"}).get_text().strip()
    recipe["recipe_rating_cnt"] = recipe_detail_soup.find("span", {"class": "stars__count"}).get_text().strip()
    recipe["recipe_author"] = recipe_detail_soup.find_all("a", {"class": "author__link author__link--name link-mask"})[2].get_text().strip()
    recipe["recipe_time"] = recipe_detail_soup.find("p", {"class": "b-recipe-info__info item-icon u-print"}).get_text().strip().replace('\n', '.').replace('\t', '.').replace('\xa0', ' ')
    recipe["recipe_created"] = recipe_detail_soup.find("p", {"class": "b-recipe-info__info item-icon"}).get_text().strip()
    recipe["recipe_comment_cnt"] = recipe_detail_soup.find("a", {"class": "b-recipe-info__link item-icon"}).get_text().strip()

    ingredients = recipe_detail_soup.find("div", {"class": "b-parameters b-parameters--ingredients u-mb-sm b-highlight u-last-m0"})

    ingredient_dict = {}
    ingredient_dict["recipe_id"] = i

    serve_cnt = ingredients.find("span", {"class": "b-parameters__amount"})
    if (serve_cnt is not None):
                recipe["serve_cnt"] = serve_cnt.get_text()

    serve_unit = ingredients.find("span", {"data-portions-target": "unit"})
    if (serve_unit is not None):
        recipe["serve_unit"] = serve_unit.get_text()


    ingredient_nutrition_url = "https://www.toprecepty.cz" + recipe_detail_soup.find("a", {"class": "b-parameters__btn b-parameters__btn--modal btn btn--block"})["href"]
    ingredient_nutrition_html = urlopen(ingredient_nutrition_url).read()
    ingredient_nutrition_soup = BeautifulSoup(ingredient_nutrition_html, features="html.parser")

    recipe["ingredient_nutrition_url"] = ingredient_nutrition_url

    grid = ingredient_nutrition_soup.find_all("table")

    nutrition_table_html = grid[0]
    ingredient_table_html = grid[1]

    with open("nutritions.html", "w", encoding='utf-8') as nutritions_file:
        nutritions_file.write(str(nutrition_table_html))

    with open("ingredients.html", "w", encoding='utf-8') as ingredients_file:
        ingredients_file.write(str(ingredient_table_html))
    
    print(recipe)
#
#    ingredient_items = ingredients.find_all("p", {"class": "b-parameters__item"})
#
#    ingredient_list = []
#    recipe_ingredient_id = 1
#    for item in ingredient_items:
#        ingredient_dict = {"id": recipe_ingredient_id}
#        ingredient_dict["recipe_id"] = i
#
#        ingredient_amount = item.find("span", {"data-portions-target": "value"})
#        if (ingredient_amount is not None):
#            ingredient_dict["ingredient_unit"] = ingredient_amount.get_text(strip=True)
#        
#        ingredient_name = item.find("span")
#        if (ingredient_name is not None):
#            ingredient_dict["ingredient_name"] = ingredient_name.contents[-1].strip()
#
#        ingredient_section = item.find("label", {"class": "b-parameters__label"})
#        if (ingredient_section is not None):
#            ingredient_section_label = ingredient_section.get_text()
#        ingredient_dict["ingredient_section"] = ingredient_section_label
#        
#        ingredient_list.append(ingredient_dict)
#
#        recipe_ingredient_id = recipe_ingredient_id + 1
#
    #nutrition_items = ingredients.find_all("p", {"class": "b-parameters__item"})
#
    #nutrition_list = []
    #recipe_nutrition_id = 1
    #for item in ingredient_items:
    #     pass

#print(recipe)
#print(ingredient_list)
#
#with open("ingredients.json", "w", encoding='utf-8') as ingredients_file:
#    ingredients_file.write(str(ingredient_list))

#print(ingredient_name)
#print(ingredient_name.contents[-1].strip())
#    i = i + 1