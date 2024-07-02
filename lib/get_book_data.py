from bs4 import BeautifulSoup
from lib.parse_url import get_base_url


def get_title(soup):
    return soup.h1.string


def get_category(soup):
    all_links = soup.find_all("a")
    return all_links[3].string


def get_description(soup):
    # use meta tag because it is unique is the page
    # and the same as the descritpion in <p> tag
    meta_description = soup.find("meta", attrs={"name": "description"})
    return meta_description["content"].strip()


def get_product_informations(soup, book):
    """
    Extract product informations from a BeautifulSoup object and add it to a book dictionary.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML of the book's page.
    book (dict): A dictionary containing information about the book.

    Returns:
    dict: The updated book dictionary, with product information added.

    Raises:
    None

    Examples:
    >>> soup = BeautifulSoup(html, 'html.parser')
    >>> book = {'Title': 'The Grand Design', 'Category': 'Art'}
    >>> get_product_information(soup, book)
    {
        'Title': 'The Grand Design',
        'Category': 'Art',
        'UPC': '9780552778147',
        'Price (excl. tax)':'£25.83',
        'Price (incl. tax)': '£25.83',
        'Availability': 'In stock (22 available)'
    }
    """
    table = soup.find("table")
    all_th = table.find_all("th")
    all_td = table.find_all("td")

    for th, td in zip(all_th, all_td):
        # exclude useless infos
        if (
            th.string == "Product Type"
            or th.string == "Number of reviews"
            or th.string == "Tax"
        ):
            continue
        book[th.string] = td.string

    return book


def get_raiting(soup):
    """
    Extract the rating of a book from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML of the book's page.

    Returns:
    int: The rating of the book, as a number between 1 and 5.

    Raises:
    None

    Examples:
    >>> soup = BeautifulSoup(html, 'html.parser')
    >>> get_rating(soup)
    4
    """
    # it is a personnal preference to use numbers rather than words
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    # find raiting
    all_text = soup.find_all("p", class_="star-rating")
    # exemple: all_text = <p class="star-rating Three">, we need to get 'Three' in that string
    current_book_ratings = all_text[0]["class"][1]
    return ratings[current_book_ratings]


def get_image_url(soup, url):
    """
    Extract the URL of the book's image from a BeautifulSoup object and a base URL.

    Parameters:
    soup (BeautifulSoup): A BeautifulSoup object containing the parsed HTML of the book's page.
    url (str): The base URL of the website.

    Returns:
    str: The URL of the book's image.

    Raises:
    None

    Examples:
    >>> soup = BeautifulSoup(html, 'html.parser')
    >>> url = 'http://books.toscrape.com/catalogue/the-grand-design_405/index.html'
    >>> get_image_url(soup, url)
    'http://books.toscrape.com/media/cache/9b/69/9b696c2064d6ee387774b6121bb4be91.jpg'
    """
    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all("img")
    current_book_img = all_img[0]

    # get the image url, remove useless characters ('../')
    # and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img["src"].lstrip("../")
    base_url = get_base_url(url)
    return f"{base_url}/{current_book_img_url}"


def get_book_data(page, url):
    """
    Extract book data from a given webpage and return a dictionary containing the data.

    Parameters:
    page (str): The HTML content of the webpage (got using get_html function).
    url (str): The URL of the webpage.

    Returns:
    dict:
        A dictionary containing the book data,
        including the title, category, description, UPC, prices, availability, rating, image URL, and page URL.

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
    book = {}
    soup = BeautifulSoup(page, "html.parser")

    # get book's title
    book["Title"] = get_title(soup)

    # get category
    book["Category"] = get_category(soup)

    # get book's description :
    book["Description"] = get_description(soup)

    # get product infos (UPC, Prices, Availability) on the book,
    get_product_informations(soup, book)

    # get review raiting,
    book["Rating"] = f"{get_raiting(soup)} out of 5"

    # get the book's imagine url
    book["Image_url"] = get_image_url(soup, url)

    return book
