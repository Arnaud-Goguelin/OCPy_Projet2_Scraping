import sys
from urllib.parse import urlparse


def get_valid_domain_url(url):
    """
    Parse a given url and return the scheme and netloc

    Parameters:
    url (string):
        the given url to parse and from wich get scheme and netloc.
        It must be a valid URL string

    Returns:
    string: containing the scheme and netloc of the input url

    Raises:
    Raises ValueErrors if scheme or domain are different

    Exemple:
    >>> url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"
    >>> get_base_url(url)
    'http://books.toscrape.com/'
    """
    try:
        parsed_url = urlparse(url)
        if parsed_url.scheme != "http":
            raise ValueError("URL must start with 'http:'")
        elif parsed_url.netloc != "books.toscrape.com":
            raise ValueError("Domain name must be 'books.toscrape.com'")
        else:
            domain_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            return domain_url
    except ValueError as error:
        print(f'An error happened about url: {error}')
        return sys.exit(1)


def get_valid_domain_and_path_url(url):
    """
    Parse a given url and return the schemen the betloc and the first element of the path

    Parameters:
    url (string):
        the given url to parse and from wich get scheme and netloc.
        It must be a valid URL string

    Returns:
    string: containing the scheme, netloc and the first element of the path of the input url

    Raises:
    Raises ValueErrors if scheme, domain or path are different

    Exemple:
    >>> url = "http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html"
    >>> get_base_from_category_url(url)
    'http://books.toscrape.com/catalogue'
    """
    try:
        domain_path = get_valid_domain_url(url)
        parsed_url = urlparse(url)
        current_path = parsed_url.path
        catalogue_path = current_path.split("/")[1]
        if catalogue_path != "catalogue":
            raise ValueError("url's path must start with 'catalogue'")
        else:
            domain_and_path_url = f"{domain_path}/{catalogue_path}"
            return domain_and_path_url
    except ValueError as error:
        print(f'An error happened about url: {error}')
        return sys.exit(1)
