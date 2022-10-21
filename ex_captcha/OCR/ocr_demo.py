# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-21
# @file    : ocr_demo.py
# @function: OCR识别实战
"""
识别图片验证码，自动登录
"""


import time
import re
import tesserocr
from selenium import webdriver
from io import BytesIO
from PIL import Image
from retrying import retry
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import numpy as np


def preprocess(image: Image):
    """
    对验证码图片做去噪处理
    :param image:
    :return:
    """
    image = image.convert('L')
    array = np.array(image)
    array = np.where(array > 100, 255, 0)
    image = Image.fromarray(array.astype('uint8'))
    return image


@retry(stop_max_attempt_number=10, retry_on_result=lambda x: x is False)
def login():
    """
    Selenium控制，OCR识别验证码，登录
    :return:
    """
    browser.get('https://captcha7.scrape.center/')
    browser.find_element(By.CSS_SELECTOR, '.username input[type="text"]').send_keys('admin')
    browser.find_element(By.CSS_SELECTOR, '.password input[type="password"]').send_keys('admin')
    captcha = browser.find_element(By.CSS_SELECTOR, '#captcha')
    image = Image.open(BytesIO(captcha.screenshot_as_png))  # 找到并截取验证码图片，转化为图片对象
    image = preprocess(image)
    captcha = tesserocr.image_to_text(image)
    captcha = re.sub('[^A-Za-z0-9]', '', captcha)  # 去除识别结果中的一些非字母字符和数字字符
    print(captcha)
    browser.find_element(By.CSS_SELECTOR, '.captcha input[type="text"]').send_keys(captcha)
    browser.find_element(By.CSS_SELECTOR, '.login').click()
    try:
        WebDriverWait(browser, 5).until(ec.presence_of_element_located((By.XPATH, '//h2[@class="text-center"]')))
        print('yes!')
        time.sleep(5)
        browser.close()
        return True
    except TimeoutException:
        print('No!')
        return False


if __name__ == '__main__':
    browser = webdriver.Chrome()
    login()
