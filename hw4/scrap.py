import math
import re
import sys
from datetime import datetime

import pandas as pd
from hh import scrap_pages
from pymongo import MongoClient
from zeep import Client

df_hh_raw = './hh.csv'
df_sj_raw = './sj.csv'
df_dest = './parsed.csv'

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['jobs-hw']
date_format = '%Y-%m-%d'

rate_client = Client('https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL')

cur_rates = {}


def get_rate_for(currency):
    if currency in cur_rates:
        return cur_rates[currency]

    money = client.service.GetCursOnDate(datetime.today().strftime(date_format))
    list_money = money._value_1._value_1
    for item in list_money:
        for v in item.values():
            if v.VchCode == currency:
                cur_rates[currency] = item['ValuteCursOnDate']['Vcurs']

    if currency not in cur_rates:
        return -1


def parse_offer(offer):
    res = [0, 0]
    if offer and offer == offer:
        o = offer.replace(u'\xa0', '').replace(' ', '')
        res = re.findall(r'\d+', o)
    if len(res) == 1:
        if offer.find('до') != -1:
            res.insert(0, 0)
        else:
            res.append(0)

    currency = re.match(r'EUR|USD|AUD|CHF|CAD|GBP', str(offer).upper())
    if currency:
        res = list(map(lambda x: int(x) * currency.group(0), res))
    return res


def process_hh_df():
    df = pd.read_csv(df_hh_raw)
    df['offer_from'] = df['offer'].apply(lambda x: parse_offer(x))
    df['offer_to'] = df['offer_from'].apply(lambda x: x[1])
    df['offer_from'] = df['offer_from'].apply(lambda x: x[0])
    del df['offer']

    df.to_csv(df_dest, index=False)


def update_db():
    df = pd.read_csv(df_dest)

    db.updates.insert_one({'timestamp': datetime.now()})

    for rec in df.to_dict('records'):
        was_replaced = db.jobs.find_one_and_replace({'link': rec['link']}, rec)
        if not was_replaced:
            db.jobs.insert_one(rec)


def filter_offer(offer):
    for x in db.jobs \
            .find({'offer_from': {'$gte': offer}}) \
            .sort('offer_from', -1):
        if x['offer_to'] != 0 and x['offer_to'] >= offer:
            print(x['offer_from'], f"до {x['offer_to']}", x['position'], x['link'], '-'.join([] * 10), sep='\n')


# EXAMPLE:
# py scrap.py "java python c# web" 2
# or to get jobs with salary more than x
# py scrap.py offer 100000
if __name__ == '__main__':
    if sys.argv[1] == 'offer':
        filter_offer(int(sys.argv[2]))
    else:
        lang = f' {sys.argv[1]}' if len(sys.argv) > 1 else ''
        pages = int(sys.argv[2]) if len(sys.argv) > 2 else math.inf

        scrap_pages(lang, pages)
        process_hh_df()
        update_db()
