# 筛选出没有爬取成功的twitter url

import pandas as pd

all_df = pd.read_csv('./url_list.csv', engine='python')
finished_df = pd.read_csv('./20220817-twitter-url-landing_page.csv', engine='python')
finished_df = finished_df[['url']]

diff_df = pd.concat([all_df, finished_df], ignore_index=True).drop_duplicates(keep=False)
diff_df.to_csv('./twitter_incomplete.csv', index=False)
