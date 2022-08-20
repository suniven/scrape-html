# for twitter url such as 'https://t.co/OdOwqOGVGp'

import os
import re
import time
import datetime
import lxml
from seleniumwire import webdriver
from sqlalchemy import Column, String, create_engine, Integer
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects import mysql
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import and_, asc, desc, or_
from common.model import WebpageInfo
import common.logger as logger
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup

sqlconn = 'mysql+pymysql://root:1101syw@localhost:3306/youtube_twitter_url?charset=utf8mb4'
_logger = logger.Logger('info')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}


def visit(browser, url, vpn):
    # 创建存储该webpage内容的文件夹
    file_save_folder = './data_twitter/' + url.split('/')[-1] + '/' + vpn
    if not os.path.exists(file_save_folder):
        os.makedirs(file_save_folder)
    else:
        if os.path.exists(file_save_folder + '/' + url.split('/')[-1] + '_redirect_info.txt'):
            print("已访问")
            return

    # visit url
    try:
        print('Time: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        browser.get(url)
    except:
        _logger.error('Failed to visit ' + url)
        del browser.requests
        return

    # 等待页面加载完成并截图
    try:
        timeout = time.time() + 10  # 10 seconds from now
        while True:
            try:
                loadingState = browser.execute_script("return document.readyState")
            except:
                loadingState = ''
            if loadingState == 'loading':
                time.sleep(1)
            elif loadingState == 'interactive' or loadingState == 'complete' or time.time() > timeout:
                break
    except:
        _logger.error("Fail to load page: " + url)

    try:
        landing_page_url = browser.current_url
        if url == landing_page_url:  # 短链接没跳转
            del browser.requests
            return
        with open(file_save_folder + '/' + url.split('/')[-1] + '_landing_page_url.txt', 'a', encoding='utf-8')as f:
            f.write(landing_page_url + '\n')
        # intermediate_urls
        # Access requests via the `requests` attribute
        intermediate_urls = ''
        for request in browser.requests:
            if request.response:
                if int(request.response.status_code / 100) == 3:  # 301 302 303 307 308
                    if request.url == url or request.response.headers['location'] == landing_page_url:
                        continue
                    intermediate_urls += "{0}\t{1}\t{2}\n".format(request.response.status_code, request.url,
                                                                  request.response.headers['location'])
                    print(
                        request.response.status_code,
                        request.url,
                        request.response.headers['location']
                    )
        if intermediate_urls:
            with open(file_save_folder + '/' + url.split('/')[-1] + '_redirect_info.txt', 'w') as f:
                f.write(intermediate_urls)
        # 清除缓存 防止temp文件占用空间
        del browser.requests
    except Exception as error:
        del browser.requests
        _logger.error("Failed to get info of {0}! {1}".format(url, error))
        del browser.requests


def main():
    seleniumwire_options = {
        'proxy': {
            'http': 'http://127.0.0.1:1080',
            'https': 'http://127.0.0.1:1080',
        },
        'request_storage_base_dir': './storage/selenium-wire-request/'
    }
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--window-size=1920,1080")
    browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options, chrome_options=chrome_options)
    # browser.maximize_window()
    browser.implicitly_wait(6)
    try:
        df = pd.read_csv('./url_split/' + sys.argv[1] + '.csv', engine='python')
        url_list = df.iloc[:, 0].values
        vpn = sys.argv[2]
        for index, url in enumerate(url_list):
            try:
                print("Index_{0}: {1}".format(index, url))
                visit(browser, url, vpn)
                del browser.requests
            except Exception as error:
                _logger.error(error)
    except Exception as error:
        del browser.requests
        _logger.error(error)
    finally:
        del browser.requests
        browser.close()
        browser.quit()


if __name__ == '__main__':
    main()
