# -*- coding: utf-8 -*-

import time
import logging
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

__author__ = 'lpe234'

username_ = 'username'
password_ = 'password'

logging.basicConfig(level=logging.INFO)

browser = webdriver.Firefox()
href = 'http://s.weibo.com/'
browser.get(href)
time.sleep(1)

# 右上登陆
login_btn = browser.find_element_by_xpath('//a[@node-type="loginBtn"]')
login_btn.click()
time.sleep(1)

# 选择账号登录
name_login = browser.find_element_by_xpath('//a[@action-data="tabname=login"]')
name_login.click()
time.sleep(1)

# 输入用户名,密码
username = browser.find_element_by_xpath('//input[@node-type="username"]')
password = browser.find_element_by_xpath('//input[@node-type="password"]')
username.clear()
username.send_keys(username_)
password.clear()
password.send_keys(password_)


# 提交登陆
sub_btn = browser.find_element_by_xpath('//a[@suda-data="key=tblog_weibologin3&value=click_sign"]')
sub_btn.click()


while True:
    try:
        verify_img = browser.find_element_by_xpath('//img[@node-type="verifycode_image"]')
    except NoSuchElementException:
        break
    if verify_img:
        # 输入验证码
        verify_code = browser.find_element_by_xpath('//input[@node-type="verifycode"]')
        verify_code_ = raw_input('verify_code > ')
        verify_code.clear()
        verify_code.send_keys(verify_code_)

        # 提交登陆
        sub_btn = browser.find_element_by_xpath('//a[@suda-data="key=tblog_weibologin3&value=click_sign"]')
        sub_btn.click()
        time.sleep(2)
    else:
        break


# 进行搜索
search_form = browser.find_element_by_xpath('//input[@class="searchInp_form"]')
search_form.clear()
search_text = raw_input('search_text > ')
search_form.send_keys(search_text.decode('utf-8'))
# 点击搜索
search_btn = browser.find_element_by_xpath('//a[@class="searchBtn"]')
search_btn.click()

# 这块可以得到具体的网页信息
count = 1
logging.info('try download html for : {}'.format(search_text))
while True:
    # 保存网页
    with open('{}-{}.html'.format(search_text, count), mode='w') as f:
        f.write(browser.page_source)
    logging.info('for page {}'.format(count))

    try:
        next_page = browser.find_element_by_css_selector('a.next')
        next_page.click()
        count += 1
        time.sleep(2)
    except NoSuchElementException, e:
        logging.error(e)
        break

