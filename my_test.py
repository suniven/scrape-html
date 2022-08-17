import pandas as pd
import os
import re


# 重命名图片 添加landing page域名信息
def rename(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith(".png"):
                id = root.split('\\')[-2]
                if f.startswith(id):
                    fullname = os.path.join(root, f)
                    try:
                        domain = df.loc[df['url'] == 'https://t.co/' + id, :].iloc[0, 1].split('/')[2]
                        if ':' in domain:  # 有端口号
                            domain = re.sub(r'\:[0-9]+', '', domain)
                    except:
                        domain = 'none'
                    re_name = id + '_' + domain + '_screenshot.png'
                    re_name_path = os.path.join(root, re_name)
                    if not os.path.exists(re_name_path):
                        os.rename(fullname, re_name_path)
                        print("重命名：", re_name_path)
                    else:
                        print("已存在")
                # print(root, f, fullname)


df = pd.read_csv('./20220817-twitter-url-landing_page.csv', engine='python')
rename('F:\\Project\\YouTube Twitter URL data\\')

# # 合并URLcsv文件
#
# def find_all_files(base):
#     for root, ds, fs in os.walk(base):
#         for f in fs:
#             if f.endswith(".csv"):
#                 fullname = os.path.join(root, f)
#                 yield fullname
#
#
# def join():
#     new_df = pd.DataFrame()
#     for file in find_all_files('F:\\db-url-landing_page\\'):
#         df = pd.read_csv(file, encoding='utf-8', engine='python')
#         new_df = pd.concat([df, new_df], ignore_index=True)
#
#     new_df.to_csv('F:\\db-url-landing_page\\20220817-twitter-url-landing_page.csv', index=False,
#                   columns=['url', 'landing_page'])
#
#
# join()

# import pandas as pd
# import os

# white_list = ['twitter.com', 'google.com', 'facebook.com',
#               'instagram.com', 'youtube.com', 'youtu.be', 'gmail.com']

# def main():
#     url_df = pd.read_csv('./urls_unique.csv',
#                          encoding='utf-8', engine='python')
#     filter_df = url_df[~url_df['domain'].isin(white_list)]
#     filter_df.to_csv('./urls_unique_filter.csv', index=False)

# if __name__ == '__main__':
#     main()

# import os
# import re
# import time
# import datetime
# import lxml
# from seleniumwire import webdriver
# from sqlalchemy import Column, String, create_engine, Integer
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects import mysql
# from sqlalchemy.pool import NullPool
# from sqlalchemy.sql import and_, asc, desc, or_
# from common.model import WebpageInfo
# import common.logger as logger
# import sys
# import pandas as pd
# import requests
# from bs4 import BeautifulSoup

# seleniumwire_options = {
#     'proxy': {
#         'http': 'http://127.0.0.1:10809',
#         'https': 'http://127.0.0.1:10809',
#     },
#     'request_storage_base_dir': './storage/selenium-wire-request/'
# }
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument("--window-size=1920,1080")
# browser = webdriver.Chrome(seleniumwire_options=seleniumwire_options, chrome_options=chrome_options)
# # browser.maximize_window()
# browser.implicitly_wait(10)
# browser.get('https://youtube.com')
# time.sleep(4)
# browser.close()
# browser.quit()

# import pandas as pd
#
#
# def main():
#     start = 0
#     step = 2000
#     csv_file_path = './url_list.csv'
#     save_path = './url_split/'
#     url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python', na_values='null')
#     # url_df = url_df.reindex(columns=url_df.columns.tolist() + ["redirect_url"])
#     count = url_df.shape[0]
#     i = 1
#     while count > 0:
#         if count < step:
#             end = url_df.shape[0]
#         else:
#             end = start + step
#         # block_df = url_df.iloc[start:end, :]
#         # block_df.to_csv(save_path + "{0}.csv".format(i), index=False)
#         with open(save_path + 'records.txt', 'a') as f:
#             f.write("{0}: {1}-{2}\n".format(i, start, end - 1))
#         i += 1
#         count -= step
#         start = end
#
#
# if __name__ == '__main__':
#     main()

# import os
# import re
# import time
# import lxml
# import requests
# from seleniumwire import webdriver
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from sqlalchemy import Column, String, create_engine, Integer
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.dialects import mysql
# from sqlalchemy.sql import and_, asc, desc, or_
# from common.model import WebpageInfo
# import common.logger as logger
# from bs4 import BeautifulSoup
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
# import json
#
# #
# # options = webdriver.ChromeOptions()
# # prefs = {
# #     "profile.managed_default_content_settings.images": 1,
# # }
# # options.add_experimental_option('prefs', prefs)
# # #
# # # # 方法1
# # # # capabilities = DesiredCapabilities.CHROME
# # # # capabilities['loggingPrefs'] = {"performance","all"}
# # # # self.driver = webdriver.Chrome(
# # # #     desired_capabilities=capabilities
# # # # )
# # #
# # # 方法2
# # options.add_experimental_option("excludeSwitches", ['enable-automation'])  # window.navigator.webdriver设置为undefined，逃过网站的防爬检查,headless无效
# # desired_capabilities = options.to_capabilities()  # 将功能添加到options中
# # desired_capabilities['loggingPrefs'] = {
# #     "performance": "ALL"  # 添加日志
# # }
# # driver = webdriver.Chrome(
# #     desired_capabilities=desired_capabilities
# # )
# #
# # driver = webdriver.Chrome()
# # driver.maximize_window()
# # try:
# #     url = 'https://t.co/GMu9zd5Q2V'
# #     driver.get(url)
# #     print(driver.get_log('performance'))
# #     print('-' * 60)
# #     print(driver.get_log('performance'))
# #     for entry in driver.get_log('performance'):
# #         params = json.loads(entry.get('message')).get('message')
# #         print(params.get('request'))  # 请求连接 包含错误连接
# #         print(params.get('response'))  # 响应连接 正确有返回值得连接
# # except:
# #     print("Error")
# # finally:
# #     driver.close()
# #     driver.quit()
#
# options = {
#     'proxy': {
#         'http': 'http://127.0.0.1:10809',
#         'https': 'http://127.0.0.1:10809',
#     }
# }
# driver = webdriver.Chrome(seleniumwire_options=options)
# driver.maximize_window()
# driver.implicitly_wait(15)
#
# try:
#     driver.get('https://t.co/GMu9zd5Q2V')
#     print("---Load Successfully---")
#     time.sleep(2)
#     # Access requests via the `requests` attribute
#     for request in driver.requests:
#         if request.response:
#             if int(request.response.status_code / 100) == 3:  # 301 302 303 307 308
#                 print(
#                     request.url,
#                     request.response.status_code,
#                     request.response.headers['location'],
#                     # request.response.headers['Content-Type']
#                 )
# except:
#     print("...")
# finally:
#     driver.close()
#     driver.quit()
#     print("?")
