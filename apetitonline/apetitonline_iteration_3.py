# pip install beautifulsoup4
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.apetitonline.cz/recepty"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")

articles = soup.find_all("article", {"class": "a-teaser content_recipe"})

receipt_list = []
for article in articles:
    receipt_name = article.find("div", {"class": "a-teaser__content"}).find("span").get_text().strip()
    receipt_link = "https://www.apetitonline.cz" + article.find("a", {"class": "a-teaser__link"})["href"]
    receipt_image = "https://www.apetitonline.cz" + article.find("img")["src"]

    #receipt_difficulty = article.find("i", {"class": "icon-difficulty-1"}).get_text()
    receipt_rating = article.find("div", {"class": "e-rating"})["data-rating-average"]
    receipt_stars = article.find("div", {"class": "e-rating"})["data-stars"]

    receipt_data_items = article.find_all("span", {"class": "a-teaser__data-item"})
    for receipt_data in receipt_data_items:
        if ("icon-stopwatch" in str(receipt_data)):
            receipt_time = receipt_data.get_text().strip()
        if ("icon-difficulty" in str(receipt_data)):
            receipt_difficulty = receipt_data.get_text().strip()

    receipt_dict = {
        "receipt_name": receipt_name,
        "receipt_link": receipt_link,
        "receipt_image": receipt_image,
        "receipt_rating": receipt_rating,
        "receipt_stars": receipt_stars,
        "receipt_time": receipt_time,
        "receipt_difficulty": receipt_difficulty
    }

    receipt_list.append(receipt_dict)

i = 1
for receipt in receipt_list:
    receipt_detail_html = urlopen(receipt["receipt_link"]).read()
    receipt_detail_soup = BeautifulSoup(receipt_detail_html, features="html.parser")
    
    with open("article_details_" + str(i) + ".html", "w", encoding='utf-8') as article_details_file:
        article_details_file.write(str(receipt_detail_soup))

    i = i + 1

