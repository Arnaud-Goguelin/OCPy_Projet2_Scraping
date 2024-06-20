from lib.parse_url import get_url_base
def get_book_infos(soup, book, url):
    # get book's title
    book['title'] = soup.h1.string

    # get book's description : 
    # use meta tag because it is unique is the page and the same as the descritpion in <p> tag
    meta_description = soup.find('meta', attrs={'name': 'description'})
    description = meta_description['content'].strip()
    book['description'] = description

    # get more infos (UPC, Prices, Tax, Availability) on the book, 
    # exclude useless infos
    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            th = tr.find_all('th')
            td = tr.find_all('td')
            if th[0].get_text() == 'Product Type' or th[0].get_text() =='Number of reviews':
                continue
            book[th[0].get_text()] = td[0].get_text()
    
    # get the book's imagine (the first in all the img tag)
    all_img = soup.find_all('img')
    current_book_img = all_img[0]
    # get the image url, remove useless characters ('../') and concatenate it with the basic url of the website
    # in order to get a valide url to use
    current_book_img_url = current_book_img['src'].lstrip('../')
    base_url = get_url_base(url)
    book['image_url'] = f'{base_url}/{current_book_img_url}'

    return book

    
