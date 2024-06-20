from bs4 import BeautifulSoup
from lib.parse_url import get_base_url, get_base_url_from_category
from lib.extract_data import extract_data
def get_book_infos(page, book, url):

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

    # get more infos (UPC, Prices, Tax, Availability) on the book, 
    # exclude useless infos
    table = soup.find('table')
    all_th = table.find_all('th')
    all_td = table.find_all('td')
    for (th, td) in zip(all_th, all_td):
        if th.string == 'Product Type' or th.string =='Number of reviews' or th.string =='Tax':
            continue
        book[th.string] = td.string

    # get review raiting
    ratings = {
    'One': 1,
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5
    }
    all_text = soup.find_all('p', class_='star-rating')
    current_book_ratings = all_text[0]['class'][1]
    rating = ratings[current_book_ratings]
    book['Rating'] = f'{rating}/5'
  
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

def get_category_infos(page, url):

    base_url = get_base_url_from_category(url)

    soup = BeautifulSoup(page, "html.parser")
    section = soup.find('section')
    lvl3_titles = section.find_all('h3')

    urls_from_category=[]
    for title in lvl3_titles:
        relative_link = title.find('a')
        reusable_link = relative_link['href'].lstrip('../')
        urls_from_category.append(f'{base_url}/{reusable_link}')
    
    for url_from_category in urls_from_category:
        book = {}
        one_book_page = extract_data(url_from_category)
        book['Book_page_url'] = url_from_category
        get_book_infos(one_book_page, book, url_from_category)
        print(book)
        print('\n\n')