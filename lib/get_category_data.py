from bs4 import BeautifulSoup

from lib.get_book_data import get_book_data
from lib.utils.get_html import get_html
from lib.utils.get_images import get_images
from lib.utils.parse_url import get_base_from_category_url


def get_page_urls(page, url):
    """
    Extract the URLs of all pages in a category from a BeautifulSoup object and a base URL.

    Parameters:
    page (str): The HTML content of the first page of the category.
    url (str): The url of the category page.

    Returns:
    list: A list of URLs of all pages in the category.

    Raises:
    None

    Examples:
    >>> page = '<html>...</html>'
    >>> url = 'http://books.toscrape.com/catalogue/category/books/art_5/index.html'
    >>> get_page_urls(page, url)
    [
        'http://books.toscrape.com/catalogue/category/books/art_5/index.html',
        'http://books.toscrape.com/catalogue/category/books/art_5/page-2.html',
        'http://books.toscrape.com/catalogue/category/books/art_5/page-3.html',
        ...
    ]
    """
    # add the current page to the list
    ulrs_to_scrap = [url]

    # check if there is several pages in the current category
    soup = BeautifulSoup(page, "html.parser")
    next_link = soup.find("a", string="next")
    # while there is an other page, get the next page url...
    while next_link:
        if next_link is None:
            break
        next_page_url = ulrs_to_scrap[0].replace("index.html", next_link["href"])
        ulrs_to_scrap.append(next_page_url)
        # ... and check again if there is a next page
        next_page = get_html(next_page_url)
        new_soup = BeautifulSoup(next_page, "html.parser")
        next_link = new_soup.find("a", string="next")

    # give feed back in console
    print("Got all pages' URLs in category")
    return ulrs_to_scrap


def get_books_url(ulrs_to_scrap, url):
    """
    Extract the URLs of all books in a category from a list of URLs to scrape and a base URL.

    Parameters:
    urls_to_scrap (list): A list of URLs of pages in a category.
    url (str): The url of the category page.

    Returns:
    list: A list of URLs of all books in the category.

    Raises:
    None

    Examples:
    >>> urls_to_scrap = ['http://books.toscrape.com/catalogue/category/books/art_5/index.html', 'http://books.toscrape.com/catalogue/category/books/art_5/page-2.html']
    >>> url = 'http://books.toscrape.com/catalogue/category/books/art_5/index.html'
    >>> get_books_url(urls_to_scrap, url)
    ['http://books.toscrape.com/catalogue/the-grand-design_405/index.html', 'http://books.toscrape.com/catalogue/sharp-objects_997/index.html', ...]
    """
    books_urls_in_category = []
    # get base url in category page in order to create usable urls to scrap books
    base_url = get_base_from_category_url(url)

    # get every link to a book in each page of the current category
    for url_to_scrap in ulrs_to_scrap:
        page_to_scrap = get_html(url_to_scrap)
        parsed_page = BeautifulSoup(page_to_scrap, "html.parser")
        section = parsed_page.find("section")
        lvl3_titles = section.find_all("h3")

        # transform every link in to a usable url, removing useless characters (../)
        # and concatenating it with the base_url (made with scheme + netloc + catalogue path)
        for title in lvl3_titles:
            relative_link = title.find("a")
            reusable_link = relative_link["href"].lstrip("../")
            books_urls_in_category.append(f"{base_url}/{reusable_link}")

    # give feed back in console
    print("Got all books' url in category")
    return books_urls_in_category


def get_books_data_in_category(books_urls_in_category):
    """
    Extract book data from a list of book URLs in a category and return a list of dictionaries containing the data.

    Parameters:
    books_urls_in_category (list): A list of URLs of books in a category.

    Returns:
    list: A list of dictionaries, where each dictionary contains the book data for a book in the category.

    Raises:
    None

    Examples:
    >>> url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
    >>> page = get_html(url)
    >>> get_book_data(page, url)
    {
        'Title': 'The Grand Design',
        'Category': 'Science',
        'Description': 'THE FIRST MAJOR WORK IN NEARLY A DECADE BY ONE OF THE...',
        'UPC': '3213b1f13f5f0f7c',
        'Price (excl. tax)': '£13.76',
        'Price (incl. tax)': '£13.76',
        'Availability': 'In stock (5 available)',
        'Rating': '3 out of 5',
        'Image_url': 'http://books.toscrape.com/media/cache/9b/69/9b696c2064d6ee387774b6121bb4be91.jpg',
        'Book_page_url': 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
    }
    """
    books_from_category = []
    # get book's data for each book in current category (same logic as in get_book_data.py)
    for book_url in books_urls_in_category:
        book_page = get_html(book_url)
        book = get_book_data(book_page, book_url)
        book["Book_page_url"] = book_url
        books_from_category.append(book)
        # give feed back in console
        print(
            f"{books_urls_in_category.index(book_url) + 1} book(s) scrapped on {len(books_urls_in_category)} in {book["Category"]} category"
        )


def get_category_data(page, url):
    """
    Extract book data from all pages of a given category and return a list of dictionaries containing the data.
        First check is there is other pages thank to presence of a link 'next'.
        While 'next' exist create every url page of the given category.
        Then get on every page the links to every book's page and determine every book's page's url.
        Scrap book's data from book's page.

    Parameters:
    page (str): The HTML content of the first page of the category (got using get_html function).
    url (str): The URL of the first page of the category.

    Returns:
    list: A list of dictionaries, where each dictionary contains the book data for a book in the category.

    Raises:
    None

    Examples:
    >>> url = "http://books.toscrape.com/catalogue/category/books/[category_name]/index.html"
    >>> page = get_html(url)
    >>> get_category_data(page, url)
    [
        {
            'Title': 'The Grand Design',
            'Category': 'Science',
            'Description': 'THE FIRST MAJOR WORK IN NEARLY A DECADE BY ONE OF THE [...]',
            'UPC': '3213b1f13f5f0f7c',
            'Price (excl. tax)': '£13.76',
            'Price (incl. tax)': '£13.76',
            'Availability': 'In stock (5 available)',
            'Rating': '3 out of 5',
            'Image_url': 'http://books.toscrape.com/media/cache/9b/69/9b696c2064d6ee387774b6121bb4be91.jpg',
            'Book_page_url': 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
        },
        {
            'Title': 'The Elegant Universe: Superstrings, Hidden Dimensions, and the Quest for the Ultimate Theory',
            'Category': 'Science',
            'Description': 'The international bestseller that inspired a major Nova special and sparked a new [...]',
            'UPC': 'c6bf14cb901c63ac',
            'Price (excl. tax)': '£13.03',
            'Price (incl. tax)': '£13.03',
            'Availability': 'In stock (3 available)',
            'Rating': '4 out of 5',
            'Image_url': 'http://books.toscrape.com/media/cache/5e/db/5edba3f8d50df6306bc5aa3f2516bd0c.jpg',
            'Book_page_url':
                'http://books.toscrape.com/catalogue/the-elegant-universe-superstrings-hidden-dimensions-and-the-quest-for-the-ultimate-theory_245/index.html'
        },
        ...
    ]
    """
    # get all pages' url from a category
    ulrs_to_scrap = get_page_urls(page, url)

    # get all books' url from all category's pages
    books_urls_in_category = get_books_url(ulrs_to_scrap, url)

    # get data for every book in a category thanks to created urls above
    books_from_category = get_books_data_in_category(books_urls_in_category)

    # get each book's image in current category and downloaded it
    get_images(books_from_category)

    return books_from_category
