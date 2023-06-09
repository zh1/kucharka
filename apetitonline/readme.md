# Stahovani a parsovani dat z apetitonline.cz
Pro prehlednost jsem rozdelil kod do nekolika casti, jednotlive `.py` soubory. Kazdy Python script resi urcitou cast stahovani pripadne parsovani urcite casti dat.

Pro parsovani HTML jazyka, ve kterem jsou "napsany" internetove stranky pouzivam Python knihovnu `BeautifulSoup`.

## Skript apetitonline_iteration_1.py
Nejprve nactu knihovny/moduly, ktere budeme ve skriptu potrebovat.
* `urllib` by mel byt soucasti defaultni instalace Pythonu
* `bs4` je modul pro parsovani informaci z HTML
  * pro instalaci budete muset v prikazove radce spustit nasledujici prikaz `pip install beautifulsoup4`

```python
from urllib.request import urlopen
from bs4 import BeautifulSoup
```

V dalsim kroku se pripojim na stranku [https://www.apetitonline.cz/recepty], promenna `url`. Nactu zdrojovy kod stranky do promenne `html`, radek 5. Nakonec do promenne `soup` naparsuju kod stranky, abych mohl pouzivat funkcionalitu `BeautifulSoup`.

```python
url = "https://www.apetitonline.cz/recepty"
html = urlopen(url).read()
soup = BeautifulSoup(html, features="html.parser")
```

Abych si udelal obrazek o tom, jak HTML kod vypada a kde hledat informace, ktere me zajimaji, ulozim si zdrojovy kod stranky do souboru na disk.

```python
with open("first_page.html", "w", encoding='utf-8') as first_page_file:
    first_page_file.write(str(soup.prettify()))
```

Kdyz jsem prozkoumal zdrojovy kod stranky, zjistil jsem, ze dulezite informace jsou ulozeny v HTML tazich `<article class="a-teaser content_recipe">`. Nasledujicim prikazem vyhledam vsechny tyto tagy a ulozim je do promenne typu seznam `articles`. Tuto promennou potom zase pro prehlednost ulozim do souboru, vystup muzete videt v repozitari v souboru `articles.html`.

```python
articles = soup.find_all("article", {"class": "a-teaser content_recipe"})

with open("articles.html", "w", encoding='utf-8') as articles_file:
    articles_file.write(str(articles))
```

## Skript apetitonline_iteration_2.py
Tento skript je az po radek 11 stejny jako `apetitonline_iteration_2.py`, nacte vsechny HTML tagy typu `article` do promenne typu pole.

Nasleduje `for` cyklus ktery prochazi vsechny polozky ze seznamu `articles` a pomoci `find()` metody dohledava jednotlive polozky, ktere chceme ukladat z hlavniho seznamu receptu.
* nazev receptu
* url receptu
* url k obrazku receptu
* hodnoceni receptu
* pocet hvezdicek

```python
for article in articles:
    receipt_name = article.find("div", {"class": "a-teaser__content"}).find("span").get_text()
    receipt_link = article.find("a", {"class": "a-teaser__link"})["href"]
    receipt_image = article.find("img")["src"]

    #receipt_difficulty = article.find("i", {"class": "icon-difficulty-1"}).get_text()
    receipt_rating = article.find("div", {"class": "e-rating"})["data-rating-average"]
    receipt_stars = article.find("div", {"class": "e-rating"})["data-stars"]
```

Na hlavni strance (https://www.apetitonline.cz/recepty) jsou taky informace o delce vareni a obtiznosti receptu, ty si zase ulozim do promenne typu seznam (radek 20) a prochazim jednotlivy polozky. Pokud polozka obsahuje `"icon-stopwatch"` retezec, tak ulozim cas, pokud `"icon-difficulty"` ulozim obtiznost.

```python
receipt_data_items = article.find_all("span", {"class": "a-teaser__data-item"})
    for receipt_data in receipt_data_items:
        if ("icon-stopwatch" in str(receipt_data)):
            receipt_time = receipt_data.get_text()
        if ("icon-difficulty" in str(receipt_data)):
            receipt_difficulty = receipt_data.get_text()
```

## Skript apetitonline_iteration_3.py
Treti skript je az po radek 28 stejny jako skript predchozi. Navic pridavam pouze sretezeni s celou URL adresou na radcich 18 a 19. Ve `for` cyklu potom jeste vsechny polozky, ktery jsem vyparsoval, pridam do promenne typu dictionary a pro kazdy recept pridam tento slovnik/dictionary do promenne typu seznam `receipt_dict`.

```python
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
```

V dalsim kroku prochazim seznam z kroku predchoziho, pro kazdy recept stahnu znovu HTML kod detailu receptu a rozparsuju pomoci `BeautifulSoup`. Na prvni strane (https://www.apetitonline.cz/recepty) je 24 receptu, vic jsem zatim nezkousel. Zase, abych pochopil, jak spravne z HTML dostat informace, ulozil jsem si prvnich 24 receptu do souboru (`article_details_[i].html`).

```python
i = 1
for receipt in receipt_list:
    receipt_detail_html = urlopen(receipt["receipt_link"]).read()
    receipt_detail_soup = BeautifulSoup(receipt_detail_html, features="html.parser")
    
    with open("article_details_" + str(i) + ".html", "w", encoding='utf-8') as article_details_file:
        article_details_file.write(str(receipt_detail_soup))

    i = i + 1
```

## Skript apetitonline_iteration_4_ingredients.py
