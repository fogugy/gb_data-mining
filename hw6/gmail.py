import sys
import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from dateutil import parser

driver = webdriver.Chrome()

client = MongoClient('mongodb://127.0.0.1:27017')
db = client['gmail']
db_name = ''


def save_mail(from_, date, theme, text):
    _hash = hash((from_, date, text))
    db[db_name].update_one(
        {'_hash': _hash},
        {'$set': {
            "from": from_,
            "date": parser.parse(date),
            "theme": theme,
            "text": text,
        }},
        upsert=True,
    )


def scrap_mail(email_, password_):
    driver.get('https://mail.google.com')

    # ждем редиректа
    WebDriverWait(driver, 5).until(EC.title_contains("Gmail"))

    input_mail = driver.find_element_by_id("identifierId")
    input_mail.send_keys(email_)
    input_mail.send_keys(Keys.RETURN)

    # ждем форму для пароля
    input_pass = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"][name="password"]')))
    input_pass.send_keys(password_)
    input_pass.send_keys(Keys.RETURN)

    while True:
        try:
            mails_all = WebDriverWait(driver, 5) \
                .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.zA')))

            mails = driver.find_elements_by_css_selector('tr.zA.zE')

            for m_el in mails:
                date = m_el.find_element_by_css_selector('td.xW.xY').text
                m_el.click()

                # ну никак без этого слипа не вышло =(
                # но итерация только по новым письмам
                time.sleep(1)

                theme_el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'h2.hP')))
                from_el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, 'span.gD[email]')))
                text_el = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.ii.gt')))

                theme = theme_el.text
                from_ = from_el.text
                text = text_el.text

                save_mail(from_, date, theme, text)

                driver.back()

            next_ = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tooltip="След."]')))
            next_active = len(driver.find_elements_by_css_selector('div[data-tooltip="След."][tabindex="0"]')) > 0

            if next_active:
                actions = ActionChains(driver)
                actions.move_to_element(next_)
                actions.click(next_)
                actions.perform()
            else:
                break

        except:
            print('Loop exit')
            break


# EXAMPLE: py gmail.py yzinovev.test@gmail.com yzinovevtest0
if __name__ == '__main__':
    email = sys.argv[1]
    password = sys.argv[2]
    db_name = email

    scrap_mail(email, password)
