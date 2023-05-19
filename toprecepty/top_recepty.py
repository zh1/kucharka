from urllib.request import urlopen
from bs4 import BeautifulSoup
from pandas import DataFrame
import csv
import logging

logging.basicConfig(filename='top_recepty.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

pages = ["https://www.toprecepty.cz/vsechny_recepty.php"]

first_20_pages = []
for page_num in range(2, 500):
    page_url = "https://www.toprecepty.cz/vsechny_recepty.php?stranka=" + str(page_num)
    first_20_pages.append(page_url)

# pages = pages + first_20_pages
pages = pages[484:499]

#i = 1
i = 12126
for page in pages:
    print(page)
    logging.debug('Starting page ' + page)
    batch_id = '2-' + str(pages.index(page))

    url = page
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
            "recipe_image": recipe_image,
            "recipe_batch_id": batch_id
        }

        recipe_list.append(recipe_dict)

    recipe_list_2 = []
    ingredient_list = []
    nutrition_list = []
    tag_list = []
    step_list = []
    comment_list = []

    for recipe in recipe_list:

        recipe_detail_html = urlopen(recipe["recipe_link"]).read()
        recipe_detail_soup = BeautifulSoup(recipe_detail_html, features="html.parser")
        print(recipe["recipe_link"])
        logging.debug('Starting recipe ' + recipe["recipe_link"])

        recipe["id"] = i
        recipe["recipe_stars"] = recipe_detail_soup.find("span", {"class": "stars__rating"}).get_text().strip()
        recipe["recipe_rating_cnt"] = recipe_detail_soup.find("span", {"class": "stars__count"}).get_text().strip()
        recipe["recipe_author"] = recipe_detail_soup.find_all("a", {"class": "author__link author__link--name link-mask"})[1].get_text().strip()
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

        section_name = ""
        sections = ["Suroviny"]
        for section in recipe_sections:
            section_names = section.find("b")
            if (section_names is not None):
                section_name = section_names.get_text().strip().replace(":", "")
            sections.append(section_name)

        recipe["sections"] = sections
        recipe_list_2.append(recipe)

        recipe["favourites_cnt"] = recipe_detail_soup.find("a", {"class": "ajax b-steps__link b-steps__link--favourite item-icon"}).get_text()

        tags = recipe_detail_soup.find("div", {"class": "b-recipe-info__tags"}).find_all("li")
        for tag in tags:
            tag_dict = {}
            tag_dict["main_category_ind"] = False if tag.find("a", {"class": "tag tag--border"}) else True

            #tag.find("a").get_text()
            tag_dict["recipe_id"] = recipe["id"]
            tag_dict["name"] = tag.get_text()
            tag_list.append(tag_dict)

        steps = recipe_detail_soup.find("ol", {"class": "b-steps__list"}).find_all("li", {"class": "b-steps__item"})
        step_cnt = 1
        for step in steps:
            step_dict = {}
            step_dict["step_link"] = step.find("p", {"class": "b-steps__link-wrap"})

            step_dict["recipe_id"] = recipe["id"]
            step_dict["name"] = step.get_text()
            step_dict["order"] = step_cnt
            step_cnt = step_cnt + 1
            step_list.append(step_dict)

        comments = recipe_detail_soup.find("div", {"class": "b-comments"}).find_all("div", {"class": "b-comment"})
        for comment in comments:
            comment_dict = {}

            comment_author = comment.find("span", {"class": "author__name"})
            if (comment_author is not None):
                author = comment_author.get_text().strip().replace(":", "")
            comment_dict["author"] = author

            comment_dict["recipe_id"] = recipe["id"]

            comment_date = comment.find("p", {"class": "b-comment__date"})
            if (comment_date is not None):
                date = comment_date.get_text().strip()
            comment_dict["date"] = date

            comment_text = comment.find("div", {"class": "b-comment__content"})
            if (comment_text is not None):
                text = comment_text.get_text()
            comment_dict["text"] = text

            comment_list.append(comment_dict)

        ingredient_nutrition_url = "https://www.toprecepty.cz/nutricni-hodnoty/" + recipe["recipe_source_id"]
        ingredient_nutrition_html = urlopen(ingredient_nutrition_url).read()
        ingredient_nutrition_soup = BeautifulSoup(ingredient_nutrition_html, features="html.parser")

        recipe["ingredient_nutrition_url"] = ingredient_nutrition_url
        logging.debug('Finishing recipe ' + recipe["recipe_link"])

        grid = ingredient_nutrition_soup.find_all("table")

        nutrition_table_html = grid[0]
        ingredient_table_html = grid[1]

        ingredient_rows = ingredient_table_html.find_all("tr")
        ingredient_rows.pop(0)

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
        
        for row in nutrition_rows:
            nutrition = {}
            nutrition["recipe_id"] = recipe["id"]
            nutrition["name"] = row.find("td").get_text()
            nutrition["value"] = row.find("span").get_text()
            nutrition["unit"] = row.find("th").get_text()
            nutrition_list.append(nutrition)
        
        sections = []
        empty_table_rows = 0
        recipe = {}
        i = i + 1

        recipe_df = DataFrame(recipe_list_2)
        ingredient_df = DataFrame(ingredient_list)
        nutrition_df = DataFrame(nutrition_list)
        tag_df = DataFrame(tag_list)
        step_df = DataFrame(step_list)
        comment_df = DataFrame(comment_list)

        recipe_df.to_csv("data/recipe" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        ingredient_df.to_csv("data/ingredient" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        nutrition_df.to_csv("data/nutrition" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        tag_df.to_csv("data/tag" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        step_df.to_csv("data/step" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
        comment_df.to_csv("data/comment" + str(batch_id) + ".csv", sep=',', index=False, encoding='utf-8', quotechar='"', escapechar='\\', quoting=csv.QUOTE_ALL)
    
    logging.debug('Finishing page ' + page)
    print(page)

#print(recipe_df)
#print(ingredient_df)
#print(nutrition_df)