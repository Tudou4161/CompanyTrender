from multiprocessing import Queue, Process, Pool
import requests 
from bs4 import BeautifulSoup as bs
import re
import time as t

def crawl(query):
    start = t.time()
    origin_titles = []
    for page in range(10): 
        raw = requests.get('https://search.naver.com/search.naver?&where=news&query=' + query + '&start=' + str((page*10)+1)).text 
        html = bs(raw, 'html.parser') 
        titles = html.select('a.news_tit') 
        for title in titles: 
            header = title.text
            origin_titles.append(header)
    end = t.time() - start
    print("logic time: ", end)
    return origin_titles


print(crawl("삼성전자"))