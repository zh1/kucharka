pages = ["https://www.toprecepty.cz/vsechny_recepty.php"]

first_20_pages = []
for page_num in range(2, 500):
    page_url = "https://www.toprecepty.cz/vsechny_recepty.php?stranka=" + str(page_num)
    first_20_pages.append(page_url)

pages = pages + first_20_pages

pages = pages[484:499]

print(pages) 