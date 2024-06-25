from lib.extract_datas import extract_datas
from lib.get_datas import get_category_datas, get_book_datas, get_website_datas
from lib.export_datas import export_category_books, export_one_book, export_website_books

book_url = 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
category_url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'
website_url = 'http://books.toscrape.com/'

if __name__ == '__main__':

    book_page = extract_datas(book_url)

    book = {}
    book['Book_page_url'] = book_url
    get_book_datas(book_page, book_url, book)
    export_one_book(book)

    category_page = extract_datas(category_url)

    books_from_category = []
    get_category_datas(category_page, category_url, books_from_category)
    export_category_books(books_from_category)

    books_from_categories = []
    landing_page = extract_datas(website_url)
    get_website_datas(landing_page, website_url, books_from_categories)
    export_website_books(books_from_categories)
