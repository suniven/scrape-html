# scrape-webpage-contents
Scrape html source code, website text and take screenshots for analysis.

## twitter_scraper.py

`python twitter_scraper.py [filename] [vpn]`

`python twitter_scraper.py 0-4999 SG`

SG: Singapore

重定向记录格式：

`"{0}\t{1}\t{2}\n".format(request.response.status_code, request.url,request.response.headers['location'])`