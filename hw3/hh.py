import sys
import pandas as pd
from urllib.parse import urlencode
from bs4 import BeautifulSoup as bs

import requests

base_url = 'https://hh.ru'
headers = {'User-agent': 'Mozilla/5.0'}


def parse(html):
    return bs(html, 'html.parser')


def get_link(lang):
    options = {
        'text': f'Программист{lang}',
    }
    link = f'{base_url}/search/vacancy?{urlencode(options)}'
    print('Entry page')
    print(link)
    return link


def get_entry_page(lang):
    link = get_link(lang)
    html = requests.get(link, headers=headers).text
    return html


def scrap_pages(lang):
    html = get_entry_page(lang)
    doc = parse(html)
    obj_list = load_next_page(doc)

    df = pd.DataFrame(columns=['position', 'offer', 'link'])

    for x in obj_list:
        vac_header = x.find('div', {'class': 'vacancy-serp-item__info'})
        offer = x.find('div', {'class': 'vacancy-serp-item__compensation'})
        vac = vac_header.getText()
        offer = offer.getText() if offer else ''
        link = vac_header.find('a')['href']
        df = df.append({'position': vac, 'offer': offer, 'link': link}, ignore_index=True)

    save_file(df)


def load_next_page(doc, obj_list=[]):
    obj_list.extend(doc.find_all('div', {'class': 'vacancy-serp-item'}))
    btn_next = doc.find('a', {'class': 'HH-Pager-Controls-Next'})

    if btn_next:
        next_link = btn_next['href']
        doc = parse(requests.get(base_url + next_link, headers=headers).text)
        load_next_page(doc, obj_list)

    return obj_list


def save_file(df):
    df.to_csv('hh.csv', index=False)


# EXAMPLE: py hh.py "java python c# web javascript"
if __name__ == '__main__':
    lang = f' {sys.argv[1]}' if len(sys.argv) > 1 else ''

    scrap_pages(lang)
