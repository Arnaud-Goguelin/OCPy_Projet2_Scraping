import time
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
    none
    """
    # wait 1 sec before make HTTP request in order to prevent server's limiter action
    # time.sleep(1)
    # make HTTP request
    response = requests.get(url, headers=headers)
    html = response.content
    return html
