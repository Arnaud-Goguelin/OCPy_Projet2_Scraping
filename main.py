"""
extraire les informations suivantes :
● product_page_url OK
● universal_ product_code (upc) OK
● title OK
● price_including_tax OK
● price_excluding_tax OK
● number_available OK
● product_description 
● category 
● review_rating
● image_url
"""
from bs4 import BeautifulSoup
from lib.extract_data import extract_data
from lib.get_book_infos import get_book_infos

url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"

if __name__ == '__main__':

    page = extract_data(url)
    #print(page)
    soup = BeautifulSoup(page, "html.parser")

    book = {}
    get_book_infos(soup, book)
    print(book)

# Attention à respecter les règles de scraping
# Vérifier le fichier robots.txt