from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time


def save_mail(from_, date, theme, text):
    print('NEW:')
    print(theme, from_, date, text, sep='_\n')


# def scrap_mail(mail, password):
driver = webdriver.Chrome()
driver.get('https://mail.google.com')

# ждем редиректа
WebDriverWait(driver, 5).until(EC.title_contains("Gmail"))

input_mail = driver.find_element_by_id("identifierId")
input_mail.send_keys('yzinovev.test@gmail.com')
input_mail.send_keys(Keys.RETURN)

# ждем форму для пароля
input_pass = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="password"][name="password"]')))
input_pass.send_keys('yzinovevtest0')
input_pass.send_keys(Keys.RETURN)

while True:
    try:
        mails = WebDriverWait(driver, 5) \
            .until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'tr.zA.zE')))

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
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-tooltip="След."][tabindex="0"]')))
        print(next_)
        next_.click()

    except:
        print('Loop exit')
        break

# EXAMPLE: py gmail.py yzinovev.test@gmail.com yzinovevtest0
# if __name__ == '__main__':
#     mail = sys.argv[1]
#     password = sys.argv[2]
#
#     scrap_mail(mail, password)
