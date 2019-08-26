import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# выключаем браузерный попап
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chrome_options)
driver.get('https://www.mvideo.ru/noutbuki-planshety-i-kompyutery')


def clear_popup():
    if len(driver.find_elements_by_css_selector('.flocktory-widget-overlay')) > 0 \
            and len(driver.find_elements_by_css_selector('.Widget-close')) > 0:
        driver.find_element_by_css_selector('.Widget-close').click()


WebDriverWait(driver, 5).until(EC.title_contains("М.Видео"))
clear_popup()

carousel_container = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.category-banner-slider-list.activated')))

links = list(map(lambda x: x.get_attribute('href'), carousel_container.find_elements_by_css_selector('a')))

for link in links:
    print('Page', link)
    driver.get(link)

    list_wrapper = WebDriverWait(driver, 5) \
        .until(EC.presence_of_element_located((By.CSS_SELECTOR, '.product-tiles-list-wrapper')))

    clear_popup()

    driver.execute_script('window.scrollBy(0, 600)')

    positions = list_wrapper.find_elements_by_css_selector('.c-product-tile')

    for x in positions:
        prod_link = x.find_element_by_css_selector('.sel-product-tile-title')
        prod_href = prod_link.get_attribute('href')
        prod_name = prod_link.text
        prod_cost = x.find_element_by_css_selector('.c-pdp-price__current').text
        print(prod_name, prod_cost)

    time.sleep(1)
