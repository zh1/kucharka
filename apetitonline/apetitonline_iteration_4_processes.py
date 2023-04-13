# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

with open("article_details_1.html", "r", encoding='utf-8') as article_detail_example:
    detail_example = article_detail_example.read()

soup = BeautifulSoup(detail_example, features="html.parser")

processes = soup.find_all("div", {"class": "s-recipe__process"})

#with open("ingredients_1.html", "w", encoding='utf-8') as ingredients_1_example:
#    ingredients_1_example.write(str(ingredients))
#
#with open("process_1.html", "w", encoding='utf-8') as process_1_example:
#    process_1_example.write(str(processes))

processes_list = []
for process in processes:
    process_item_list = process.find_all("div", {"class": "s-recipe__process-step"})

    for item in process_item_list:
        process_step = item.find("span", {"class": "s-recipe__process-num"}).get_text()
        process_description = item.find("div", {"class": "s-recipe__process-text e-formated-output"}).findChildren()

        print(process_step, process_description)
