import requests
def extract_data(url):

    response = requests.get(url)

    html = response.content

    return html