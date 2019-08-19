# import sys
# import pandas as pd
# from urllib.parse import urlencode
# from bs4 import BeautifulSoup as bs
# import math
# import requests
# import time
#
# base_url = 'https://www.superjob.ru'
# headers = {'User-agent': 'Mozilla/5.0'}
#
#
# def parse(html):
#     return bs(html, 'html.parser')
#
#
# def get_link(lang):
#     options = {
#         'keywords': f'Программист{lang}',
#     }
#     link = f"{base_url}/vacancy/search/?keywords={options['keywords']}"
#     print('Entry page')
#     print(link)
#     return link
#
#
# def get_entry_page(lang):
#     link = get_link(lang)
#     html = requests.get(link, headers=headers).text
#     return html
#
#
# def scrap_pages(lang, pages):
#     html = get_entry_page(lang)
#     doc = parse(html)
#     obj_list = load_next_page(doc, pages - 1)
#     # df = pd.DataFrame(columns=['position', 'offer', 'link'])
#
#     # for x in obj_list:
#     #     vac_header = x.find('div', {'class': 'vacancy-serp-item__info'})
#     #     offer = x.find('div', {'class': 'vacancy-serp-item__compensation'})
#     #     vac = vac_header.getText()
#     #     offer = offer.getText() if offer else ''
#     #     link = vac_header.find('a')['href']
#     #     df = df.append({'position': vac, 'offer': offer, 'link': link}, ignore_index=True)
#     #
#     # save_file(df)
#
#
# def load_next_page(doc, pages, obj_list=[]):
#     obj_list.extend(doc.find_all('div', {'class': '_3zucV _2GPIV i6-sc _3VcZr'}))
#     print(len(obj_list))
#     btn_next = doc.find('a', {'class': 'f-test-button-dalshe'})
#     print(pages, btn_next)
#     if pages < 1:
#         return obj_list
#
#     if btn_next:
#         next_link = btn_next['href']
#         doc = parse(requests.get(base_url + next_link, headers=headers).text)
#         load_next_page(doc, pages - 1, obj_list)
#
#     return obj_list
#
#
# def save_file(df):
#     print(df.describe())
#     df.to_csv('sj.csv', index=False)
#
#
# # EXAMPLE: py hh.py "java python c# web" 2
# if __name__ == '__main__':
#     lang = f' {sys.argv[1]}' if len(sys.argv) > 1 else ''
#     pages = int(sys.argv[2]) if len(sys.argv) > 2 else math.inf
#
#     scrap_pages(lang, pages)
