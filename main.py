from lib.extract_datas import extract_datas
from lib.get_datas import get_category_datas, get_book_datas
from lib.export_datas import export_category_books, export_one_book

one_book_url = 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
one_category_url = 'http://books.toscrape.com/catalogue/category/books/history_32/index.html'

if __name__ == '__main__':

    book_page = extract_datas(one_book_url)

    book = {}
    book['Book_page_url'] = one_book_url
    get_book_datas(book_page, one_book_url, book)
    export_one_book(book)

    category_page = extract_datas(one_category_url)

    books_from_category = []
    get_category_datas(category_page, one_category_url, books_from_category)
    export_category_books(books_from_category)
