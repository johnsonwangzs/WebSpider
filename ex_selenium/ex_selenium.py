# -*- encoding: utf-8 -*-
# @auther  : wangzs
# @time    : 2022-10-18
# @file    : ex_selenium.py
# @function: Selenium的使用。
"""
Selenium是一个自动化测试工具，利用它可以驱动浏览器完成特定的操作（点击、下拉等），还可以获取浏览器当前呈现的页面的源代码
非常适合爬取一些JavaScript动态渲染的页面。
需要先安装Chrome浏览器，并配置好ChromeDriver。
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()


class BrowserGet:
    def work(self):
        browser.get('https://www.baidu.com')
        input = browser.find_element(by='id', value='kw')
        input.send_keys('Python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)


if __name__ == '__main__':
    browserGet = BrowserGet()
    browserGet.work()