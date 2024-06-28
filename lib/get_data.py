from bs4 import BeautifulSoup
from lib.parse_url import (
    get_base_url,
    get_base_url_from_category,
)
from lib.get_html import get_html


def get_book_data(page, url):
    book = {}
    soup = BeautifulSoup(page, "html.parser")

    # get book's title
    book["Title"] = soup.h1.string

    # get category
    all_links = soup.find_all("a")
    book["Category"] = all_links[3].string

    # get book's description :
    # use meta tag because it is unique is the page
    # and the same as the descritpion in <p> tag
    meta_description = soup.find("meta", attrs={"name": "description"})
    description = meta_description["content"].strip()
    book["Description"] = description

    # get more infos (UPC, Prices, Availability) on the book,
    # exclude useless infos
    table = soup.find("table")
    all_th = table.find_all("th")
    all_td = table.find_all("td")
    for th, td in zip(all_th, all_td):
        if (
            th.string == "Product Type"
            or th.string == "Number of reviews"
            or th.string == "Tax"
        ):
            continue
        book[th.string] = td.string

    # get review raiting,
    # it is a personnal preference to use numbers rather than words
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    all_text = soup.find_all("p", class_="star-rating")
    current_book_ratings = all_text[0]["class"][1]
    rating = ratings[current_book_ratings]
    book["Rating"] = f"{rating} out of 5"

    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all("img")
    current_book_img = all_img[0]

    # get the image url, remove useless characters ('../')
    # and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img["src"].lstrip("../")
    base_url = get_base_url(url)
    book["Image_url"] = f"{base_url}/{current_book_img_url}"

    return book


def get_category_data(page, url):
    books_from_category = []
    # get all pages' url from a category
    all_ulrs_to_scrap = [url]
    soup = BeautifulSoup(page, "html.parser")
    next_link = soup.find("a", string="next")

    while next_link:
        if next_link is None:
            break
        next_page_url = all_ulrs_to_scrap[0].replace("index.html", next_link["href"])
        all_ulrs_to_scrap.append(next_page_url)

        next_page = get_html(next_page_url)
        new_soup = BeautifulSoup(next_page, "html.parser")
        next_link = new_soup.find("a", string="next")
    print("Got all pages' urls in category")

    # get base url in category page in order to create usable urls to scrap books
    base_url = get_base_url_from_category(url)

    # get all books' url from all category's pages
    urls_from_category = []

    for url_to_scrap in all_ulrs_to_scrap:
        page_to_scrap = get_html(url_to_scrap)
        parsed_page = BeautifulSoup(page_to_scrap, "html.parser")
        section = parsed_page.find("section")
        lvl3_titles = section.find_all("h3")

        for title in lvl3_titles:
            relative_link = title.find("a")
            # create usable urls from links scraped
            reusable_link = relative_link["href"].lstrip("../")
            urls_from_category.append(f"{base_url}/{reusable_link}")

    print("Got all books' url in category")

    # get data for every book in a category thanks to created urls above
    for url_from_category in urls_from_category:
        one_book_page = get_html(url_from_category)
        book = get_book_data(one_book_page, url_from_category)
        book["Book_page_url"] = url_from_category
        books_from_category.append(book)
        print(f'{urls_from_category.index(url_from_category) + 1} book(s) scrapped on {len(urls_from_category)}')

    return books_from_category


def get_website_data(page, url):
    books_from_website = []
    soup = BeautifulSoup(page, "html.parser")
    # get all categories links except the first one wich is a link to all books
    categories_link = soup.find("aside").find_all("a")[1:]

    # get all categories urls in order to scrap books from each category
    # thanks to function get_category_datas above
    categories_url = []
    for category_link in categories_link:
        categories_url.append(f"{url}{category_link['href']}")
    print("Got all categories' url from website")

    # scrap books from each category
    for category_url in categories_url:
        print(f'start to scrap category n°{categories_url.index(category_url) + 1} on {len(categories_url)} \n')
        category_page = get_html(category_url)
        books_from_website = get_category_data(category_page, category_url)
        print(f'{categories_url.index(category_url) + 1} category(ies) scrapped on {len(categories_url)} \n')

    return books_from_website
