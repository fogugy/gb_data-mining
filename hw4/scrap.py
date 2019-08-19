import sys
import math
import pandas as pd
import re
from hh import scrap_pages


def parse_offer(offer, usd_rur):
    res = ['0']
    if offer and offer == offer:
        o = offer.replace(u'\xa0', '').replace(' ', '')
        res = re.findall(r'\d+', o)
    if str(offer).lower().find('usd') != -1:
        res = list(map(lambda x: int(x)*usd_rur,res))
    return res


def process_hh_df(usd_rur):
    df = pd.read_csv('./hh.csv')
    df['offer_from'] = df['offer'].apply(lambda x: parse_offer(x, usd_rur))
    df['offer_to'] = df['offer_from'].apply(lambda x: x[1] if len(x) > 1 else 0)
    df['offer_from'] = df['offer_from'].apply(lambda x: x[0])
    del df['offer']

    df.to_csv('./parsed.csv', index=False)


# EXAMPLE: py scrap.py "java python c# web" 65 2
if __name__ == '__main__':
    lang = f' {sys.argv[1]}' if len(sys.argv) > 1 else ''
    usd_rur = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    pages = int(sys.argv[3]) if len(sys.argv) > 3 else math.inf

    scrap_pages(lang, pages)
    process_hh_df(usd_rur)
