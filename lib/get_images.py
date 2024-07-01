import time
import wget
import os
import re

from lib.get_time import get_time


def slugify(string):
    """
    Parameters:
    string (string): a valide string to slugify

    Returns:
    return a string friendly with URL

    Raises:
    none
    """
    string = string.lower().strip()
    string = re.sub(r'[^\w\s-]', '', string)
    string = re.sub(r'[\s-]+', '_', string)
    string = re.sub(r'^-+|-+$', '', string)
    return string


def get_images(books):
    """
    return a file download from an URL

    Parameters:
    url (string): a valide URL of the file to download

    Returns:
    filename where URL is downloaded to

    Raises:
    none
    """
    parent_dir = "images"
    print(f'images download begins at {get_time()}')
    for book in books:
        directory = book["Category"]
        path = os.path.join(parent_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)

        image_format = book["Image_url"].split(".")[-1]
        slugified_title = slugify(book["Title"])

        filename = f'{books.index(book)+1}_{slugified_title}.{image_format}'

        destination_path = os.path.join(path, filename)
        if not os.path.exists(destination_path):
            time.sleep(1)
            wget.download(book["Image_url"], destination_path)
            print(f'\n{books.index(book)+1} image(s) donwloaded on {len(books)} in {book["Category"]} category')
        else:
            print(f'\nbook n°{books.index(book)+1}\'s image already donwloaded in {book["Category"]} category')

    return print(f'All category\'s images downloaded, downloading ends at {get_time()}')
