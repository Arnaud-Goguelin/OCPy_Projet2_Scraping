from lib.extract_data import extract_data

url = "http://books.toscrape.com/catalogue/the-grand-design_405/index.html"

if __name__ == '__main__':

    html = extract_data(url)
    print(html)