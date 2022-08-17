import pandas as pd


def main():
    start = 0
    step = 2000
    csv_file_path = './twitter_incomplete.csv'
    save_path = './url_split_twitter_re_scrape/'
    url_df = pd.read_csv(csv_file_path, encoding='utf-8', engine='python', na_values='null')
    # url_df = url_df.reindex(columns=url_df.columns.tolist() + ["redirect_url"])
    count = url_df.shape[0]
    i = 1
    while count > 0:
        if count < step:
            end = url_df.shape[0]
        else:
            end = start + step
        block_df = url_df.iloc[start:end, :]
        block_df.to_csv(save_path + "{0}.csv".format(i), index=False)
        i += 1
        count -= step
        start = end


if __name__ == '__main__':
    main()
