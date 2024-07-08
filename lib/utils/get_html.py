import time
import sys
import requests


headers = {
    "User-Agent": "python-requests/2.32.3",
    "From": "Arnaud Goguelin, student at OpenClassrooms",
}


def get_html(url):
    """
    make a HTTP request to a given url and return the response content

    Parameters:
    url (string): the given url where to make a request

    Returns:
    bytes: the content of the response

    Raises:
    detects all types of errors likely to occur during an HTTP request
    return error message and exit app.
    """
    try:
        # wait 1 sec before make HTTP request in order to prevent server's limiter action
        # time.sleep(1)
        # make HTTP request
        response = requests.get(url, headers=headers)
        # raise exception if status code is not 200
        response.raise_for_status()
        html = response.content
        return html
    except requests.exceptions.RequestException as error:
        print("Request failed. Here is the response:"
              f'\n   status: {response.status_code}'
              f'\n   message: {str(error)}')
        return sys.exit(1)
