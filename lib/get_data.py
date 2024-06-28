from bs4 import BeautifulSoup
from lib.parse_url import (
    get_base_url,
    get_base_from_category_url,
)
from lib.get_html import get_html


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
    book["Title"] = soup.h1.string

    # get category
    all_links = soup.find_all("a")
    book["Category"] = all_links[3].string

    # get book's description :
    # use meta tag because it is unique is the page
    # and the same as the descritpion in <p> tag
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"].strip()
    book["Description"] = description

    # get more infos (UPC, Prices, Availability) on the book,
    # exclude useless infos
    table = soup.find("table")
    all_th = table.find_all("th")
    all_td = table.find_all("td")
    for th, td in zip(all_th, all_td):
        if (
            th.string == "Product Type"
            or th.string == "Number of reviews"
            or th.string == "Tax"
        ):
            continue
        book[th.string] = td.string

    # get review raiting,
    # it is a personnal preference to use numbers rather than words
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    all_text = soup.find_all("p", class_="star-rating")
    current_book_ratings = all_text[0]["class"][1]
    rating = ratings[current_book_ratings]
    book["Rating"] = f"{rating} out of 5"

    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all("img")
    current_book_img = all_img[0]

    # get the image url, remove useless characters ('../')
    # and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img["src"].lstrip("../")
    base_url = get_base_url(url)
    book["Image_url"] = f"{base_url}/{current_book_img_url}"

    return book


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
    books_from_category = []
    # get all pages' url from a category
    all_ulrs_to_scrap = [url]
    soup = BeautifulSoup(page, "html.parser")
    next_link = soup.find("a", string="next")

    while next_link:
        if next_link is None:
            break
        next_page_url = all_ulrs_to_scrap[0].replace("index.html", next_link["href"])
        all_ulrs_to_scrap.append(next_page_url)

        next_page = get_html(next_page_url)
        new_soup = BeautifulSoup(next_page, "html.parser")
        next_link = new_soup.find("a", string="next")
    print("Got all pages' urls in category")

    # get base url in category page in order to create usable urls to scrap books
    base_url = get_base_from_category_url(url)

    # get all books' url from all category's pages
    urls_from_category = []

    for url_to_scrap in all_ulrs_to_scrap:
        page_to_scrap = get_html(url_to_scrap)
        parsed_page = BeautifulSoup(page_to_scrap, "html.parser")
        section = parsed_page.find("section")
        lvl3_titles = section.find_all("h3")

        for title in lvl3_titles:
            relative_link = title.find("a")
            # create usable urls from links scraped
            reusable_link = relative_link["href"].lstrip("../")
            urls_from_category.append(f"{base_url}/{reusable_link}")

    print("Got all books' url in category")

    # get data for every book in a category thanks to created urls above
    for url_from_category in urls_from_category:
        one_book_page = get_html(url_from_category)
        book = get_book_data(one_book_page, url_from_category)
        book["Book_page_url"] = url_from_category
        books_from_category.append(book)
        print(
            f"{urls_from_category.index(url_from_category) + 1} book(s) scrapped on {len(urls_from_category)}"
        )

    return books_from_category


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
    books_from_website = []
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
    for category_url in categories_url:
        print(
            f"start to scrap category n°{categories_url.index(category_url) + 1} on {len(categories_url)} \n"
        )
        category_page = get_html(category_url)
        books_from_website = get_category_data(category_page, category_url)
        print(
            f"{categories_url.index(category_url) + 1} category(ies) scrapped on {len(categories_url)} \n"
        )

    return books_from_website
