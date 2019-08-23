import math
import sys
from datetime import datetime, date, timedelta

from bson.decimal128 import Decimal128
from pymongo import MongoClient
from zeep import Client

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['cb']

url = 'https://www.cbr.ru/DailyInfoWebServ/DailyInfo.asmx?WSDL'
client = Client(url)
date_format = '%Y-%m-%d'


def get_currency_for_date(currency, from_, to_):
    d_from = datetime.strptime(from_, date_format)
    d_to = datetime.strptime(to_, date_format)

    for day_index in range((d_to - d_from).days):
        cur_date = d_from + timedelta(days=day_index)
        cur_date_str = cur_date.strftime(date_format)
        money = client.service.GetCursOnDate(cur_date_str)
        list_money = money._value_1._value_1
        for item in list_money:
            for v in item.values():
                if v.VchCode == currency:
                    rec = {
                        'date': cur_date,
                        'value': Decimal128(item['ValuteCursOnDate']['Vcurs']),
                    }
                    db[currency].update_one(
                        {'date': rec['date']},
                        {'$set': rec},
                        upsert=True,
                    )


def get_currency_difference(currency, from_, to_):
    get_currency_for_date(currency, from_, to_)
    d_from = datetime.strptime(from_, date_format)
    d_to = datetime.strptime(to_, date_format)

    max_ = 0.0
    min_ = math.inf
    date_min = None
    date_max = None
    for x in db[currency].find({'date': {'$gte': d_from, '$lte': d_to}}).sort('date'):
        val = x['value'].to_decimal()
        if max_ < val:
            max_ = val
            date_max = x['date']
        if min_ > val:
            min_ = val
            date_min = x['date']

    delta = max_ - min_
    return date_max, date_min, delta


# EXAMPLE: py rub_rate.py AUD 2019-02-01 2019-02-10
if __name__ == "__main__":
    today = date.today()
    currency = sys.argv[1] if len(sys.argv) > 1 else 'USD'
    from_ = sys.argv[2] if len(sys.argv) > 2 else today
    to_ = sys.argv[3] if len(sys.argv) > 3 else today

    date_max, date_min, delta = get_currency_difference(currency, from_, to_)

    print(f'Валюту {currency} надо было покупать {date_min.strftime(date_format)}', end=' ')
    print(f'а продавать {date_max.strftime(date_format)}')
    print('Прибыль:', delta)
