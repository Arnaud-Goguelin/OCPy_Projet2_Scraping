from urllib.parse import urlparse


def get_base_url(url):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    return base_url


def get_base_url_from_category(url):
    parsed_url = urlparse(url)
    current_path = parsed_url.path
    book_from_category_path = current_path.split('/')
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}/{book_from_category_path[1]}"
    return base_url
