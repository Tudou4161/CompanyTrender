from multiprocessing import Queue, Process, Pool
import multiprocessing
import requests 
from bs4 import BeautifulSoup as bs
import time as t

Q = Queue()

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
    Q.put(origin_titles)

if __name__ == "__main__":
    p = Pool(multiprocessing.cpu_count())
    p.map(crawl, ("삼성전자"))
    print(Q.get())
    p.close()
    p.join()