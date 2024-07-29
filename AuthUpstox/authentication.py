from .auth_config import *

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp
import requests
from urllib.parse import parse_qs, urlparse
import warnings
warnings.filterwarnings("ignore")

def get_auth_code(user_mob_no, totp_code, user_pin):
    auth_code = None

    driver = webdriver.Edge()    
    driver.get(login_url)

    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mobileNum"]'))
        )
        mob_no_input = driver.find_element(By.XPATH, '//*[@id="mobileNum"]')
        mob_no_input.send_keys(user_mob_no)
        driver.find_element(By.XPATH, '//*[@id="getOtp"]').click()
    except:
        print('Page loading failed')

    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="otpNum"]'))
        )
        totp_input = driver.find_element(By.XPATH, '//*[@id="otpNum"]')
        totp = pyotp.TOTP(totp_code)
        totp_input.send_keys("{}".format(totp.now()))
        driver.find_element(By.XPATH, '//*[@id="continueBtn"]').click()
    except:
        print('Page loading failed')

    try:
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pinCode"]'))
        )
        pin_input = driver.find_element(By.XPATH, '//*[@id="pinCode"]')
        pin_input.send_keys(user_pin)
        driver.find_element(By.XPATH, '//*[@id="pinContinueBtn"]').click()
    except:
        print('Page loading failed')

    try:
        element = WebDriverWait(driver, 60).until(
            EC.url_changes(driver.current_url))
        final_url = driver.current_url

        parsed = urlparse(final_url)
        auth_code = parse_qs(parsed.query)['code'][0]
    except:
        print('Page loading failed')

    driver.quit()

    return auth_code

def get_access_token(auth_code, api_key, api_secret, redirect_uri, access_token_url):
    access_token = None
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = {
        'code': auth_code,
        'client_id': api_key,
        'client_secret': api_secret,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(access_token_url, headers=headers, data=data)

    if response.status_code == 200: # Request was successful
        access_token = response.json().get('access_token')
    else: # Request failed
        print("Error:", response.status_code, response.text)

    return access_token

def get_profile(access_token, profile_url):
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(profile_url, headers=headers)

    if response.status_code == 200: # Request was successful
        profile_data = response.json()
    else: # Request failed
        print("Error:", response.status_code, response.text)

    return True if profile_data['status'] == 'success' else False, profile_data['data']

def get_margin(access_token, funds_margin_url):
    headers = {
        'accept': 'application/json',
        'Api-Version': '2.0',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(funds_margin_url, headers=headers)

    if response.status_code == 200: # Request was successful
        fund_margin_data = response.json()
    else: # Request failed
        print("Error:", response.status_code, response.text)

    return True if fund_margin_data['status'] == 'success' else False, fund_margin_data['data']

def authenticate():
    auth_code = get_auth_code(user_mob_no, totp_code, user_pin)
    if auth_code == None:
        raise ValueError('Not able to generate Authentication Code')
    else:
        access_token = get_access_token(auth_code, api_key, api_secret, redirect_uri, access_token_url)
        if access_token == None:
            raise ValueError('Not able to generate Access Token')
        else:
            bool_val, profile_det = get_profile(access_token, profile_url)
            _, fund_margin_det = get_margin(access_token, funds_margin_url)
            return bool_val, profile_det, fund_margin_det
