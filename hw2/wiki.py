import re
import sys
import pandas as pd
from lxml import html
from pprint import pprint

import requests


def get_link(topic):
    link = 'https://ru.wikipedia.org/wiki/' + topic.capitalize()
    return link


def get_topic_page(topic):
    link = get_link(topic)
    html = requests.get(link).text
    return html


def get_topic_text(topic):
    link = get_link(topic)
    return get_page_text(link)


def get_page_text(url):
    html_content = requests.get(url).text
    words = re.findall("[а-яА-Я]{3,}", html_content)
    return words


def get_common_words(words):
    rate = {}
    for word in words:
        if word in rate:
            rate[word] += 1
        else:
            rate[word] = 1
    rate_list = list(rate.items())
    rate_list.sort(key=lambda x: -x[1])
    return rate_list


def get_topic_links(topic):
    html_text = get_topic_page(topic)
    dom = html.fromstring(html_text)
    links_ul = dom.get_element_by_id('Ссылки').getparent().getnext().getnext().getnext()
    links = list(map(lambda x: x.get('href'), links_ul.cssselect('a')))
    return links


def get_topic_links_text(topic):
    links = get_topic_links(topic)
    words = []
    for link in links:
        w_ = get_page_text(link)
        words.extend(w_)
        print(link, len(w_))
    return words


if __name__ == '__main__':
    topic = sys.argv[1]
    get_common_words(get_topic_links_text(topic))
