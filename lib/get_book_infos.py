def get_book_infos(soup, book):
    book['title'] = soup.title.string

    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            th = tr.find_all('th')
            td = tr.find_all('td')
            book[th[0].get_text()] = td[0].get_text()
    
    return book

    
