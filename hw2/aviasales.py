import json
import sys

import requests


def get_city_iata(from_city, to_city):
    url = f'https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{from_city}%20в%20{to_city}'
    req = requests.get(url)
    data = json.loads(req.text)
    return data['origin']['iata'], data['destination']['iata']


def flight_info(from_city, to_city):
    from_iata, to_iata = get_city_iata(from_city, to_city)
    service = 'http://min-prices.aviasales.ru/calendar_preload?'
    link = f'{service}origin={from_iata}&destination={to_iata}&one_way=true'
    req = requests.get(link)
    data = json.loads(req.text)
    return data


def print_flight_data(origin, destination, data, top=-1):
    best_prices = data['best_prices']
    if top > 0:
        best_prices = best_prices[:top]

    print(origin, '->', destination)
    print('Цена', 'Отправление', 'Аэропорт', sep='\t')
    for x in sorted(best_prices, key=lambda x: x['value']):
        print(x['value'], x['depart_date'], x['gate'], sep='\t')


# EXAMPLE: py aviasales.py Москва Саратов 5
if __name__ == '__main__':
    origin = sys.argv[1]
    destination = sys.argv[2]
    top = -1

    if len(sys.argv) > 3:
        top = int(sys.argv[3])

    dt = flight_info(origin, destination)
    print_flight_data(origin, destination, dt, top)
