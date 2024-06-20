from lib.extract_data import extract_data
from lib.get_book_infos import get_book_infos
from lib.export_data import export_data_in_csv

url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"

if __name__ == '__main__':

    page = extract_data(url)

    book = {}
    book['Book_page_url'] = url
    get_book_infos(page, book, url)
    export_data_in_csv(book)