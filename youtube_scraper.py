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
from common.model import WebpageInfo, WebpageInfoAbs
import common.logger as logger
import sys
import pandas as pd
import requests
from bs4 import BeautifulSoup
import hashlib

sqlconn = 'mysql+pymysql://root:1101syw@localhost:3306/youtube_twitter_url?charset=utf8mb4'
_logger = logger.Logger('info')

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}
proxies = {
    'http': 'http://127.0.0.1:1080',
    'https': 'http://127.0.0.1:1080'
}


def visit(browser, DBSession, url, vpn):
    # 创建存储该webpage内容的文件夹
    url_hash = hashlib.md5(url.encode('UTF-8')).hexdigest()  # hash(url)
    url_temp = '/'.join(url.split('/')[2:])
    url_legal_name = re.sub(r'[\\/\:\*\?"<>\|]', '', url_temp)  # 替换命名规则不允许的特殊字符
    if len(url_legal_name) > 100:
        url_legal_name = url_legal_name[:100]

    file_save_folder = './data_youtube/' + url_hash + '/' + vpn
    if not os.path.exists(file_save_folder):
        os.makedirs(file_save_folder)
    else:
        if os.path.exists(file_save_folder + '/' + url_hash + '_landing_page_url.txt'):
            print("已访问")
            return

    # visit url
    try:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        browser.get(url)
    except:
        _logger.error('Failed to visit ' + url)
        # 截取失败截图
        try:
            screenshot = file_save_folder + '/_incomplete_' + url_hash + '_screenshot.png'
            if not os.path.exists(screenshot):
                browser.save_screenshot(screenshot)
                print("Fail to visit. Take Screenshot successfully.")
            else:
                print("Screenshot Already Exists.")
        except Exception as error:
            del browser.requests
            _logger.error("Failed to take screenshot: " + url)
            return
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
        try:
            try:
                domain = browser.current_url.split('/')[2]
            except:
                domain = 'none'
            screenshot = file_save_folder + '/' + url_hash + '_' + domain + '_screenshot_' + url_legal_name + '.png'
            if not os.path.exists(screenshot):
                browser.save_screenshot(screenshot)
                print("Take Screenshot successfully.")
            else:
                print("Screenshot Already Exists.")
        except Exception as error:
            _logger.error("Failed To Take Screenshots: " + url)
    except:
        _logger.error("Failed to take screenshots: " + url)

    try:
        print("插入数据库......")
        # 保存相关内容
        webpage_info = WebpageInfo()
        webpage_info.vpn = vpn
        webpage_info.url = url
        webpage_info.url_hash = url_hash
        webpage_info.html = browser.page_source
        webpage_info.text = ''
        webpage_info.landing_page = browser.current_url
        webpage_info.intermediate_urls = ''

        webpage_info_abs = WebpageInfoAbs()
        webpage_info_abs.vpn = vpn
        webpage_info_abs.url = url
        webpage_info_abs.url_hash = url_hash
        webpage_info_abs.landing_page = browser.current_url
        webpage_info_abs.intermediate_urls = ''

        # if webpage_info.url == webpage_info.landing_page:
        #     del browser.requests
        #     return
        # text
        bs = BeautifulSoup(browser.page_source, "lxml")
        text = bs.get_text()
        if text:
            webpage_info.text = text
        # 同时保存一份到文件夹
        with open(file_save_folder + '/' + url_hash + '_page_source.html', 'w', encoding='utf-8') as f:
            f.write(browser.page_source)
        with open(file_save_folder + '/' + url_hash + '_text.txt', 'w', encoding='utf-8') as f:
            f.write(text)
        with open(file_save_folder + '/' + url_hash + '_landing_page_url.txt', 'w', encoding='utf-8') as f:
            f.write(browser.current_url + '\n')
        # intermediate_urls
        # Access requests via the `requests` attribute
        intermediate_urls = ''
        for request in browser.requests:
            if request.response:
                if int(request.response.status_code / 100) == 3:  # 301 302 303 307 308
                    if request.url == url and request.response.headers['location'] == browser.current_url:
                        continue
                    intermediate_urls += "{0}\t{1}\t{2}\n".format(request.response.status_code, request.url,
                                                                  request.response.headers['location'])
                    print(
                        request.response.status_code,
                        request.url,
                        request.response.headers['location']
                    )
        if intermediate_urls:
            webpage_info.intermediate_urls = intermediate_urls
            webpage_info_abs.intermediate_urls = intermediate_urls
            # 同时保存一份到文件夹
            with open(file_save_folder + '/' + url_hash + '_redirect_info.txt', 'w') as f:
                f.write(intermediate_urls)
        # 清除缓存 防止temp文件占用空间
        del browser.requests

        session = DBSession()
        session.add(webpage_info)
        session.commit()
        session.add(webpage_info_abs)
        session.commit()
        session.close()
    except Exception as error:
        del browser.requests
        _logger.error("Failed to get info of {0}! {1}".format(url, error))
        del browser.requests

    # # 提取网页中的图片并保存
    # try:
    #     img_tags = browser.find_elements_by_tag_name('img')
    #     for img_tag in img_tags:
    #         try:
    #             img_src = img_tag.get_attribute('src')
    #             if img_src:
    #                 img_path = file_save_folder + '/' + img_src.split('/')[-1]
    #                 if not os.path.exists(img_path):
    #                     print("Getting Img: {0}".format(img_src))
    #                     r = requests.get(img_src, headers=headers, proxies=proxies, timeout=(8, 8))
    #                     with open(img_path, "wb") as f:
    #                         f.write(r.content)
    #                         print("Successfully Get Img.")
    #                 else:
    #                     print("Img Already Exists.")
    #         except Exception as error:
    #             _logger.error(error)
    # except Exception as error:
    #     _logger.info("No Img or error occurs. Error: {0}".format(error))


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

    # # headless模式
    # option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    # option.add_argument("--window-size=1920,1080")
    # browser = webdriver.Chrome(chrome_options=option)
    # browser.implicitly_wait(15)
    engine = create_engine(sqlconn, echo=True, poolclass=NullPool)
    DBSession = sessionmaker(bind=engine)
    try:
        df = pd.read_csv('./url_split_youtube/' + sys.argv[1] + '.csv', engine='python')
        url_list = df.iloc[:, 0].values
        vpn = sys.argv[2]
        for index, url in enumerate(url_list):
            try:
                print("Index_{0}: {1}".format(index, url))
                # # 查询是否已经访问过
                # session = DBSession()
                # rows = session.query(WebpageInfo).filter(WebpageInfo.url.like(url), and_(WebpageInfo.vpn.like(vpn))).all()
                # if rows:
                #     print("已访问")
                #     continue
                # session.close()
                visit(browser, DBSession, url, vpn)
                del browser.requests
            except Exception as error:
                _logger.error(error)
    except Exception as error:
        del browser.requests
        _logger.error(error)
    finally:
        del browser.requests
        engine.dispose()
        browser.close()
        browser.quit()


if __name__ == '__main__':
    main()
