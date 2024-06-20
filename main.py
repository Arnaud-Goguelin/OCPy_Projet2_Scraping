from bs4 import BeautifulSoup

from lib.extract_data import extract_data
from lib.get_book_infos import get_book_infos
from lib.get_book_infos import get_category_infos

from lib.export_data import export_one_book_in_csv

one_book_url = 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
one_category_url = 'http://books.toscrape.com/catalogue/category/books/history_32/index.html'

if __name__ == '__main__':

    #book_page = extract_data(one_book_url)

    #book = {}
    #book['Book_page_url'] = one_book_url
    #get_book_infos(book_page, book, one_book_url)
    #export_one_book_in_csv(book)

    category_page = extract_data(one_category_url)
    get_category_infos(category_page, one_category_url)
