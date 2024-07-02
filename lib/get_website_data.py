from bs4 import BeautifulSoup
from lib.get_category_data import get_category_data
from lib.utils.get_html import get_html


def get_categories_links(url):
    """
    Extract the links of all categories from hom page.

    Parameters:
    url (str): home page url.

    Returns:
    list: A list of BeautifulSoup objects representing the links of all categories.

    Raises:
    None

    Examples:
    >>> page = '<html>...</html>'
    >>> get_categories_link(page)
    [<a href="catalogue/category/books/art_5/index.html">Art</a>, <a href="catalogue/category/books/biography_7/index.html">Biography</a>, ...]
    """
    landing_page = get_html(url)
    soup = BeautifulSoup(landing_page, "html.parser")
    # get all categories links except the first one wich is a link to all books
    categories_link = soup.find("aside").find_all("a")[1:]
    return categories_link


def get_categories_urls(categories_link, url):
    """
    build the URLs of all categories thanks to a list of HTML links objects and a base URL.

    Parameters:
    categories_link (list): A list of BeautifulSoup objects representing the links of all categories.
    url (str): The base URL of the website.

    Returns:
    list: A list of URLs of all categories.

    Raises:
    None

    Examples:
    >>> categories_link =
        [
            <a href="catalogue/category/books/art_5/index.html">Art</a>,
            <a href="catalogue/category/books/biography_7/index.html">Biography</a>,
            ...
        ]
    >>> url = 'http://books.toscrape.com/'
    >>> get_categories_url(categories_link, url)
    [
        'http://books.toscrape.com/catalogue/category/books/art_5/index.html',
        'http://books.toscrape.com/catalogue/category/books/biography_7/index.html',
        ...
    ]
    """
    categories_url = []
    for category_link in categories_link:
        categories_url.append(f"{url}{category_link['href']}")
    # give feed back in console
    print("Got all categories' url from website")
    return categories_url


def get_books_data_in_website(categories_url):
    """
    Extract book data from all categories of a website and return a list of dictionaries containing the data.

    Parameters:
    categories_url (list): A list of URLs of all categories in the website.

    Returns:
    list: A list of lists of dictionaries, where each dictionary contains the book data for a book in a category.

    Raises:
    None

    Examples:
    >>> categories_url =
        [
            'http://books.toscrape.com/catalogue/category/books/art_5/index.html',
            'http://books.toscrape.com/catalogue/category/books/biography_7/index.html',
            ...
        ]
    >>> get_books_data_in_website(categories_url)
    [
        [
            {
                'Title': 'The Grand Design',
                'Category': 'Art',
                'UPC': '9780552778147',
                'Price (excl. tax)': '£25.83',
                'Price (incl. tax)': '£25.83',
                'Availability': 'In stock (22 available)',
                'Rating': 4,
                'Image_url': 'http://books.toscrape.com/media/cache/2c/da/2cdad67c44b002e7ead0cc35693c0e8b.jpg',
                'Book_page_url': 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
            },
            ...
        ],
        [
            {
                'Title': 'A Light in the Attic',
                'Category': 'Biography',
                'UPC': '9781846555207',
                'Price (excl. tax)': '£51.77',
                'Price (incl. tax)': '£51.77',
                'Availability': 'In stock (19 available)',
                'Rating': 3,
                'Image_url': 'http://books.toscrape.com/media/cache/20/37/2037044541230980070480049d75e739.jpg',
                'Book_page_url': 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
            },
            ...
        ],
        ...
    ]
    """
    books_from_website = []
    for category_url in categories_url:

        # give feed back in console
        print(
            f"start to scrap category n°{categories_url.index(category_url) + 1} on {len(categories_url)} \n"
        )

        books_from_category = get_category_data(category_url)
        books_from_website.append(books_from_category)

        # give feed back in console
        print(
            f"{categories_url.index(category_url) + 1} category(ies) scrapped on {len(categories_url)} \n"
        )

    return books_from_website


def get_website_data(url):
    """
    Extract book data from all categories of a given website and return a list of dictionaries containing the data.

    Parameters:
    url (str): The URL of the homepage of the website.

    Returns:
    list: A list of dictionaries, where each dictionary contains the book data for a book in the website.

    Raises:
    None

    Examples:
    >>> url = "http://books.toscrape.com/"
    >>> page = get_html(url)
    >>> get_website(page, url)
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
            'Title': 'A Distant Mirror: The Calamitous 14th Century',
            'Category': 'History',
            'Description': 'Barbara W. Tuchman--the acclaimed author of the Pulitzer Prize–winning classic [...]',
            'UPC': 'd5e0526e1ab682a3',
            'Price (excl. tax)': '£14.58',
            'Price (incl. tax)': '£14.58',
            'Availability': 'In stock (14 available)',
            'Rating': '3 out of 5',
            'Image_url': 'http://books.toscrape.com/media/cache/d8/0a/d80ac19cd0aef94c5ac257b1eb3c1d37.jpg',
            'Book_page_url':
                'http://books.toscrape.com/catalogue/a-distant-mirror-the-calamitous-14th-century_652/index.html'
        },
        ...
    ]
    """
    categories_link = get_categories_links(url)

    categories_url = get_categories_urls(categories_link, url)

    books_from_website = get_books_data_in_website(categories_url)

    return books_from_website
