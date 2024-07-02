import time
import wget
import os
import re

from lib.utils.get_time import get_time


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
    book (dictionnary Key(string) : Value(string)): the given books' data where to find a valide image url

    Returns:
    filename where URL is downloaded to

    Raises:
    none
    """
    parent_dir = "images"
    print(f'images download begins at {get_time()}')

    for book in books:
        # create one folder for each category if it does not exists yet
        directory = book["Category"]
        path = os.path.join(parent_dir, directory)
        if not os.path.exists(path):
            os.makedirs(path)

        # create a slugified filename for destination path
        image_format = book["Image_url"].split(".")[-1]
        slugified_title = slugify(book["Title"])

        filename = f'{books.index(book)+1}_{slugified_title}.{image_format}'

        # downloaded the book's image if it is not done yet
        destination_path = os.path.join(path, filename)
        if not os.path.exists(destination_path):
            # still wait 1 secondes between each donwloaded in order to prevent server's limiter action
            # time.sleep(1)
            wget.download(book["Image_url"], destination_path)
            print(f'\n{books.index(book)+1} image(s) donwloaded on {len(books)} in {book["Category"]} category')
        else:
            print(f'\nbook n°{books.index(book)+1}\'s image already donwloaded in {book["Category"]} category')

    return print(f'All category\'s images downloaded, downloading ends at {get_time()}')
