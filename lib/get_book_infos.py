def get_book_infos(soup, book):
    book['title'] = soup.title.string.strip()

    for table in soup.find_all('table'):
        for tr in table.find_all('tr'):
            th = tr.find_all('th')
            td = tr.find_all('td')
            #print(th[0].get_text)
            if th[0].get_text() == 'Product Type' or th[0].get_text() =='Number of reviews':
                continue
            book[th[0].get_text()] = td[0].get_text()
    
    return book

    
