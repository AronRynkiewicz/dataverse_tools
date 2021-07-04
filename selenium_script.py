from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import sys
import time
from credentials import SELENIUM


LOGIN_DATA = SELENIUM['LOGIN_DATA']

SITE_LOGIN_DATA = SELENIUM['SITE_LOGIN_DATA']


LOGIN_HOST = 'https://{}:{}@mxrdr-test.icm.edu.pl'.format(LOGIN_DATA['username'], LOGIN_DATA['password'])


CHROMIUM_PATH_DICT = {
    'win32': '\\chromium_driver\\win\\chromedriver.exe',
    'linux': '/chromium_driver/chromedriver.exe',
    'darwin': '/chromium_driver/macos/chromedriver',
}


FIELDS_XPATHS = {
    'username_field': '/html/body/div[1]/div[3]/div/div/div/div[1]/form/div[1]/div/input',
    'password_field': '/html/body/div[1]/div[3]/div/div/div/div[1]/form/div[2]/div/input',
}


BUTTONS_XPATHS = {
    'first_login_btn': '/html/body/div[1]/div[1]/div[3]/div[2]/nav/ul/li[4]/a',
    'second_login_btn': '/html/body/div[1]/div[3]/div/div/div/div[1]/form/div[3]/div/button/span',
}


FAILURE_MESSAGES = {
    'first_login_btn': ' first log in button',
    'username_field': ' username field',
    'password_field': ' password field',
    'second_login_btn': ' second log in button',
}


def configure_chromium():
    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--no-sandbox')
    options.add_argument('--verbose')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    # options.add_argument('--headless')
    return options


def button_clicker(button_XPATH, message, driver):
    try:
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, button_XPATH))
        )
        btn.click()
    except Exception:
        print('Failed to locate' + message)
        return False
    return True


def fill_login_credentials(XPATH, message, login_data, driver):
    try:
        field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, XPATH))
        )
        field.send_keys(login_data)
    except Exception:
        print('Failed to locate' + message)
        return False
    return True


def login(driver):
    first_login_btn_success = button_clicker(
        BUTTONS_XPATHS['first_login_btn'],
        FAILURE_MESSAGES['first_login_btn'],
        driver,
    )

    username_field_success = fill_login_credentials(
        FIELDS_XPATHS['username_field'],
        FAILURE_MESSAGES['username_field'],
        SITE_LOGIN_DATA['username'],
        driver,
    )

    password_field_success = fill_login_credentials(
        FIELDS_XPATHS['password_field'],
        FAILURE_MESSAGES['password_field'],
        SITE_LOGIN_DATA['password'],
        driver,
    )

    second_login_btn_success = button_clicker(
        BUTTONS_XPATHS['second_login_btn'],
        FAILURE_MESSAGES['second_login_btn'],
        driver,
    )
    
    if all([
        first_login_btn_success,
        username_field_success,
        password_field_success,
        second_login_btn_success,
    ]):
        return True
    return False


def connect():
    options = configure_chromium()

    PATH = os.getcwd() + CHROMIUM_PATH_DICT[sys.platform]
    driver = webdriver.Chrome(PATH, options=options)
    driver.get(LOGIN_HOST)

    login_success = login(driver)
    if login_success:
        print('Successful login')

    time.sleep(5)

    driver.quit()


connect()