from bs4 import BeautifulSoup
from lib.extract_data import extract_data
from lib.get_book_infos import get_book_infos

url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"

if __name__ == '__main__':

    page = extract_data(url)
    soup = BeautifulSoup(page, "html.parser")

    book = {}
    book['product_page_url'] = url
    get_book_infos(soup, book, url)
    print(book)

# Attention à respecter les règles de scraping
# Vérifier le fichier robots.txt