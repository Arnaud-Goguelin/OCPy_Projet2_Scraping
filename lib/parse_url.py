from urllib.parse import urlparse


def get_base_url(url):
    """
    Parse a given url and return the scheme and netloc

    Parameters:
    url (string):
        the given url to parse and from wich get scheme and netloc.
        It must be a valid URL string

    Returns:
    string: containing the scheme and netloc of the input url

    Raises:
    none

    Exemple:
    >>> url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
    >>> get_base_url(url)
    'http://books.toscrape.com/'
    """
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def get_base_from_category_url(url):
    """
    Parse a given url and return the schemen the betloc and the first element of the path

    Parameters:
    url (string):
        the given url to parse and from wich get scheme and netloc.
        It must be a valid URL string

    Returns:
    string: containing the scheme, netloc and the first element of the path of the input url

    Raises:
    none

    Exemple:
    >>> url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    >>> get_base_from_category_url(url)
    'http://books.toscrape.com/catalogue'
    """
    parsed_url = urlparse(url)
    current_path = parsed_url.path
    book_from_category_path = current_path.split("/")
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{book_from_category_path[1]}"

    return base_url
