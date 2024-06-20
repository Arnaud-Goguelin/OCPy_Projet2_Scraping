from bs4 import BeautifulSoup
from lib.parse_url import get_url_base
def get_book_infos(page, book, url):

    soup = BeautifulSoup(page, "html.parser")


    # get book's title
    book['title'] = soup.h1.string
    
    # get category
    all_links = soup.find_all('a')
    book['category'] = all_links[3].string

    # get book's description : 
    # use meta tag because it is unique is the page 
    # and the same as the descritpion in <p> tag
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'].strip()
    book['description'] = description

    # get more infos (UPC, Prices, Tax, Availability) on the book, 
    # exclude useless infos
    table = soup.find('table')
    all_th = table.find_all('th')
    all_td = table.find_all('td')
    for (th, td) in zip(all_th, all_td):
        if th.string == 'Product Type' or th.string =='Number of reviews':
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
    book['review_rating'] = f'{rating}/5'
  
    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all('img')
    current_book_img = all_img[0]

    # get the image url, remove useless characters ('../') 
    # and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img['src'].lstrip('../')
    base_url = get_url_base(url)
    book['image_url'] = f'{base_url}/{current_book_img_url}'

    return book