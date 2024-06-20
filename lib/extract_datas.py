import requests
def extract_datas(url):

    response = requests.get(url)

    html = response.content

    return html