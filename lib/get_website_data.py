from bs4 import BeautifulSoup
from lib import get_category_data
from lib.utils.get_html import get_html


def get_website_data(page, url):
    """
    Extract book data from all categories of a given website and return a list of dictionaries containing the data.

    Parameters:
    page (str): The HTML content of the homepage of the website (got using get_html function).
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
    soup = BeautifulSoup(page, "html.parser")
    # get all categories links except the first one wich is a link to all books
    categories_link = soup.find("aside").find_all("a")[1:]

    # get all categories urls in order to scrap books from each category
    # thanks to function get_category_datas above
    categories_url = []
    for category_link in categories_link:
        categories_url.append(f"{url}{category_link['href']}")
    print("Got all categories' url from website")

    # scrap books from each category
    books_from_website = []
    for category_url in categories_url:
        print(
            f"start to scrap category n°{categories_url.index(category_url) + 1} on {len(categories_url)} \n"
        )
        category_page = get_html(category_url)
        books_from_category = get_category_data(category_page, category_url)
        books_from_website.append(books_from_category)
        print(
            f"{categories_url.index(category_url) + 1} category(ies) scrapped on {len(categories_url)} \n"
        )
    return books_from_website
