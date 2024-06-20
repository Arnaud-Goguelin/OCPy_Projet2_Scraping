from bs4 import BeautifulSoup

from repo.lib.extract_datas import extract_datas
from repo.lib.get_datas import get_book_datas
from repo.lib.get_datas import get_category_datas

from repo.lib.export_datas import export_one_book_in_csv

one_book_url = 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
one_category_url = 'http://books.toscrape.com/catalogue/category/books/history_32/index.html'

if __name__ == '__main__':

    book_page = extract_datas(one_book_url)

    book = {}
    book['Book_page_url'] = one_book_url
    get_book_datas(book_page, book, one_book_url)
    export_one_book_in_csv(book)

    category_page = extract_datas(one_category_url)

    get_category_datas(category_page, one_category_url)
