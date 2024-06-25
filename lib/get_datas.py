from bs4 import BeautifulSoup
from lib.parse_url import get_base_url, get_base_url_from_category
from lib.extract_datas import extract_datas


def get_book_datas(page, url, book):

    soup = BeautifulSoup(page, "html.parser")

    # get book's title
    book['Title'] = soup.h1.string

    # get category
    all_links = soup.find_all('a')
    book['Category'] = all_links[3].string

    # get book's description :
    # use meta tag because it is unique is the page
    # and the same as the descritpion in <p> tag
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'].strip()
    book['Description'] = description

    # get more infos (UPC, Prices, Availability) on the book,
    # exclude useless infos
    table = soup.find('table')
    all_th = table.find_all('th')
    all_td = table.find_all('td')
    for (th, td) in zip(all_th, all_td):
        if th.string == 'Product Type' or th.string == 'Number of reviews' or th.string == 'Tax':
            continue
        book[th.string] = td.string

    # get review raiting,
    # it is a personnal preference to use numbers rather than words
    ratings = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
    all_text = soup.find_all('p', class_='star-rating')
    current_book_ratings = all_text[0]['class'][1]
    rating = ratings[current_book_ratings]
    book['Rating'] = f'{rating} out of 5'

    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all('img')
    current_book_img = all_img[0]

    # get the image url, remove useless characters ('../')
    # and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img['src'].lstrip('../')
    base_url = get_base_url(url)
    book['Image_url'] = f'{base_url}/{current_book_img_url}'

    return book


def get_category_datas(page, url, books_from_category):

    # get all pages' url from a category
    all_ulrs_to_scrap = [url]
    soup = BeautifulSoup(page, "html.parser")
    next_link = soup.find('a', string='next')

    while next_link:
        next_link_href = next_link.get('href')
        next_page_url = all_ulrs_to_scrap[0].replace('index.html', next_link_href)
        all_ulrs_to_scrap.append(next_page_url)

        next_page = extract_datas(next_page_url)
        new_soup = BeautifulSoup(next_page, 'html.parser')
        next_link = new_soup.find('a', string='next')

    # get base url in category page
    base_url = get_base_url_from_category(url)

    # get all books' url from all category's pages
    urls_from_category = []

    for url_to_scrap in all_ulrs_to_scrap:
        page_to_scrap = extract_datas(url_to_scrap)
        parsed_page = BeautifulSoup(page_to_scrap, 'html.parser')
        section = parsed_page.find('section')
        lvl3_titles = section.find_all('h3')

        for title in lvl3_titles:
            relative_link = title.find('a')
            # create usable urls from links scraped
            reusable_link = relative_link['href'].lstrip('../')
            urls_from_category.append(f'{base_url}/{reusable_link}')

    # get infos for every book in a category thanks to created urls above
    for url_from_category in urls_from_category:
        book = {}
        one_book_page = extract_datas(url_from_category)
        book['Book_page_url'] = url_from_category
        get_book_datas(one_book_page, url_from_category, book)
        books_from_category.append(book)

    return books_from_category
