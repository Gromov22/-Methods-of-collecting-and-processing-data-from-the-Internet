from selenium import webdriver
from selenium.webdriver.safari.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient

service = Service('/usr/bin/safaridriver')
driver = webdriver.Safari(service=service)
driver.maximize_window()
driver.get('https://passport.yandex.com/auth?retpath=https%3A%2F%2Fmail.yandex.com')
driver.implicitly_wait(15)

username = driver.find_element(By.ID, 'passp-field-login')
username.send_keys('test.mail.selenium@yandex.ru')
username.send_keys(Keys.ENTER)

password = driver.find_element(By.ID, 'passp-field-passwd')
password.send_keys('loli2281337')
password.send_keys(Keys.ENTER)
sleep(3)

lite_version = driver.find_elements(By.XPATH, '//a[@class="mail-ui-Link ns-action"]')
driver.get(lite_version[0].get_attribute('href'))

def message_box():
    messages = driver.find_elements(By.CLASS_NAME, 'b-messages__message')
    # wait = WebDriverWait(driver, 15)
    # next_page = wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_nb-button-text')))
    # next_page = driver.find_element(By.CLASS_NAME, '_nb-button-text')
    for message in messages:
        message.get_attribute('href')
        date = message.find_element(By.CLASS_NAME, "b-messages__date").text
        sender = message.find_element(By.XPATH, '//span/span[@class="b-messages__from__text"]').text
        theme = message.find_element(By.CLASS_NAME, 'b-messages__subject').text
        text = message.find_element(By.CLASS_NAME, 'b-messages__firstline').text
        result = {
            'Sender': sender,
            'Date': date,
            'Theme': theme.replace('\xa0', '').strip(),
            'Text': text.replace('\u200c', '').strip()
             }
        yield result


def create_database():
    client = MongoClient('localhost:27017')
    mail_db = client['mail_db']
    mail_collection = mail_db['mail_collection']
    for i in message_box():
        mail_collection.insert_one(i)

create_database()