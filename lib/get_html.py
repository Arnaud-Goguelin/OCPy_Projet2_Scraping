import time
import requests


def get_html(url):
    # wait 1 sec before make HTTP request in order to prevent server's limiter action
    time.sleep(1)
    # make HTTP request
    response = requests.get(url)
    html = response.content
    return html
