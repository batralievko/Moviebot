def refs(year, genre):
    import pandas as pd
    import requests
    from bs4 import BeautifulSoup
    # import re
    import json
    import selenium
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    import time
    import random
    from numpy import NaN as nan
    import csv
    import os
    driver = webdriver.Chrome()
    start = 'https://www.imdb.com/search/keyword/?pf_rd_m=A2FGELUUNOQJNL&\
    pf_rd_p=bdc91cb7-0144-4906-b072-b45760c8aa67&\
    pf_rd_r=PXCPH97MT3PHQD6DF4AY&pf_rd_s=right-1&pf_rd_t=15051&pf_rd_i=genre&ref_=kw_ref_yr&title_type=movie&release_date='
    year_to_year = str(year) + '%2C' + str(year)
    page = '&mode=detail&page=1&genres='
    genre_ = str(genre).title()
    end = '&sort=moviemeter,asc'
    driver = webdriver.Chrome()
    links = []
    url = start + year_to_year + page + genre_ + end
    time.sleep(random.uniform(2, 4))
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', {'class': 'lister-list'}).find_all('div', {'class': 'lister-item mode-detail'})
    for div in divs:
        a = div.find('a').get('href')
        links.append(a)

    driver = webdriver.Chrome()
    data_for_all_links = pd.DataFrame([])
    link = 'https://www.imdb.com'
    url = link + random.choice(links)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # название

    try:
        name = soup.find('div', {'class': 'originalTitle'}).text
    except AttributeError:
        try:
            divs = soup.find('div', {'class': 'title_wrapper'})
            div = soup.find('h1', {'class': ''})
            name = div.contents[0].string.strip()
        except IndexError:
            name = 'I do not remember the name. But you have to watch!'
        except AttributeError:
            name = 'I do not remember the name. But you have to watch!'
    except IndexError:
        name = nan

    # постер

    try:
        poster = soup.find('div', {'class': 'poster'})
        ref_for_im = poster.find('img').get('src')
    except AttributeError:
        poster = 'ref for mem'
    except IndexError:
        poster = 'ref for mem'

    # дата релиза

    try:
        divs = soup.find('div', {'class': 'title_wrapper'})
        div = divs.find_all('a')
        a = len(div) - 1
        b = list(div[a])
        date_release = b[0].string.strip()
    except IndexError:
        date_release = 'Old (wise) movie'
    except AttributeError:
        date_release = 'Old (wise) movie'

    # описание (синопсис)

    try:
        div = soup.find('div', {'id': 'titleStoryLine'})
        gen = div.find_all('div', {'class': 'inline canwrap'})
        data = []
        for i in gen:
            a = i.find_all('span')
            data.append(a)
        description = list(data[0][0])[0]
    except IndexError:
        description = 'It is really interesting story!'
    except AttributeError:
        description = 'It is really interesting story!'

    # длительность

    try:
        divs = soup.find('div', {'class': 'title_wrapper'})
        div = divs.find('time', {})
        run_time = div.contents[0].string.strip()
    except IndexError:
        run_time = 'approximately 1 hour'
    except AttributeError:
        run_time = 'approximately 1 hour'

    # возрастной рейтинг

    try:
        divs = soup.find('div', {'class': 'title_wrapper'})  # для возрастного рейтинга
        div = divs.find('div', {'class': 'subtext'})
        age_rating = div.contents[0].string.strip()
        if age_rating == '':
            age_rating = '16+'
        else:
            pass
    except IndexError:
        age_rating = '16+'
    except AttributeError:
        age_rating = '16+'

    # рейтинг IMdb

    try:
        div = soup.find('div', {'class': 'imdbRating'})  # рейтинг IMdb, кол-во отзывов и крит. рецензий
        imdb_rat = div.find_all('span')
        list_for_imdb_rat = []
        for i in imdb_rat:
            list_for_imdb_rat.append(i.string)
        imdb_rating = list_for_imdb_rat[0]
    except IndexError:
        imdb_rating = 'Not Bad'
    except AttributeError:
        imdb_rating = 'Not Bad'

    data = (
        [url, name, ref_for_im, date_release,
         run_time, description, age_rating, imdb_rating
         ]
    )

    col = (
        ['Unique_link', 'Name', 'Ref_for_image', 'Date_release',
         'Run_time', 'Description',
         'Age_rating',
         'Imdb_rating']
    )

    total_data = (
        (pd.DataFrame(
            data, col
        )).transpose()
    )

    return total_data