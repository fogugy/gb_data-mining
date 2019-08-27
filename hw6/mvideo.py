import sys
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# выключаем браузерный попап
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['mvideo']
db_name = ''


def save_to_db(prod_name, prod_cost, prod_href):
    db[db_name].update_one(
        {'link': prod_href},
        {'$set': {
            "name": prod_name,
            "cost": float(prod_cost),
            "link": prod_href,
        }},
        upsert=True,
    )


def clear_popup():
    if len(driver.find_elements_by_css_selector('.flocktory-widget-overlay')) > 0 \
            and len(driver.find_elements_by_css_selector('.Widget-close')) > 0:
        driver.find_element_by_css_selector('.Widget-close').click()


def scrap_positions(url):
    driver.get(url)
    WebDriverWait(driver, 5)
    clear_popup()
    driver.execute_script('window.scrollBy(0, 600)')

    positions = driver.find_elements_by_css_selector('.c-product-tile')

    for x in positions:
        prod_link = x.find_element_by_css_selector('.sel-product-tile-title')
        prod_href = prod_link.get_attribute('href')
        prod_name = prod_link.text
        prod_cost_els = x.find_elements_by_css_selector('.c-pdp-price__current')
        prod_cost = 0
        if len(prod_cost_els) > 0:
            prod_cost = prod_cost_els[0].text.replace(' ', '')[:-1]

        save_to_db(prod_name, prod_cost, prod_href)

    next_btns = driver.find_elements_by_css_selector('a.c-pagination__next:not(.disabled)')

    if len(next_btns) > 0:
        next_href = next_btns[0].get_attribute('href')
        if len(next_href) > 0:
            scrap_positions(next_href)

    time.sleep(1)


def scrap(entry):
    driver.get(entry)
    WebDriverWait(driver, 5).until(EC.title_contains("М.Видео"))
    clear_popup()

    carousel_container = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.category-banner-slider-list.activated')))

    links = list(map(lambda x: x.get_attribute('href'), carousel_container.find_elements_by_css_selector('a')))

    for link in links:
        scrap_positions(link)


if __name__ == '__main__':
    entry = sys.argv[1] if len(sys.argv) > 1 else 'https://www.mvideo.ru/noutbuki-planshety-i-kompyutery'
    db_name = sys.argv[2] if len(sys.argv) > 2 else 'noutbuki-planshety-kompyutery'

    scrap(entry)
