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

#receipt_list = []
#for article in articles:
#    receipt_name = article.find("div", {"class": "a-teaser__content"}).find("span").get_text().strip()
#    receipt_link = "https://www.apetitonline.cz" + article.find("a", {"class": "a-teaser__link"})["href"]
#    receipt_image = "https://www.apetitonline.cz" + article.find("img")["src"]
#
#    #receipt_difficulty = article.find("i", {"class": "icon-difficulty-1"}).get_text()
#    receipt_rating = article.find("div", {"class": "e-rating"})["data-rating-average"]
#    receipt_stars = article.find("div", {"class": "e-rating"})["data-stars"]
#
#    receipt_data_items = article.find_all("span", {"class": "a-teaser__data-item"})
#    for receipt_data in receipt_data_items:
#        if ("icon-stopwatch" in str(receipt_data)):
#            receipt_time = receipt_data.get_text().strip()
#        if ("icon-difficulty" in str(receipt_data)):
#            receipt_difficulty = receipt_data.get_text().strip()
#
#    receipt_dict = {
#        "receipt_name": receipt_name,
#        "receipt_link": receipt_link,
#        "receipt_image": receipt_image,
#        "receipt_rating": receipt_rating,
#        "receipt_stars": receipt_stars,
#        "receipt_time": receipt_time,
#        "receipt_difficulty": receipt_difficulty
#    }
#
#    receipt_list.append(receipt_dict)
#
#i = 1
#for receipt in receipt_list:
#    receipt_detail_html = urlopen(receipt["receipt_link"]).read()
#    receipt_detail_soup = BeautifulSoup(receipt_detail_html, features="html.parser")
#    
#    with open("article_details_" + str(i) + ".html", "w", encoding='utf-8') as article_details_file:
#        article_details_file.write(str(receipt_detail_soup))
#
#    i = i + 1
#
#