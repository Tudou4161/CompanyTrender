# app.py
from keras.preprocessing.sequence import pad_sequences
import requests 
from bs4 import BeautifulSoup as bs
import re 
from konlpy.tag import Kkma 
import numpy as np
import pickle
import tensorflow as tf
from flask import Flask, render_template, jsonify, request
import time
import datetime
from multiprocessing import Queue, Process, Pool
#Flask 객체 인스턴스 생성
app = Flask(__name__)

Q = Queue()

def clean_str(text):
    pattern = '([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)' # E-mail제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+' # URL제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '([ㄱ-ㅎㅏ-ㅣ]+)'  # 한글 자음, 모음 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '<[^>]*>'         # HTML 태그 제거
    text = re.sub(pattern=pattern, repl='', string=text)
    pattern = '[^\w\s]'         # 특수기호제거
    text = re.sub(pattern=pattern, repl='', string=text)
    return text   


def Crawler(query: str) -> list:
    start = time.time()
    origin_titles, __titles, href = [], [], []
    for page in range(10): 
        raw = requests.get('https://search.naver.com/search.naver?&where=news&query=' + query + '&start=' + str((page*10)+1)).text 
        html = bs(raw, 'html.parser') 
        titles = html.select('a.news_tit') 
        for title in titles: 
            header = title.text
            origin_titles.append(header)
            __href = title.get("href")
            clean_title = clean_str(header)
            # clean_title = re.sub('[-=+,#/\?:^ $.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', header)
            __titles.append(clean_title)
            href.append(__href)
    sec = time.time() - start
    Q.put(__titles)
    Q.put(origin_titles)
    Q.put(href[:10])
    Q.put(datetime.timedelta(seconds=sec))


def Tokenizer(headers: list) -> list:
    start = time.time()
    toEmotion, toFrequency = [], []
    stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '이', '보', '않', '없', '나', 
            '사람', '주', '아니', '등', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', 
            '일', '그렇', '위하', '때문', '그것', '두', '말하', '알', '그러나', '받', '못하', '일', '그런', 
            '또', '문제', '더', '사회', '많', '그리고', '좋', '크', '따르', '중', '나오', '가지', '씨', '시키',
            '만들', '지금', '생각하', '그러', '속', '하나', '집', '살', '모르', '적', '월', '데', '자신', '안', 
            '어떤', '내', '내', '경우', '명', '생각', '시간', '그녀', '다시', '이런', '앞', '보이', '번', '나', '뉴', '큰', '획', '긋고'
            '다른', '어떻', '여자', '개', '전', '들', '사실', '이렇', '점', '싶', '말', '정도', '좀', '원', '잘', '통하', '소리', '놓']
    kkma = Kkma()

    for header in headers:
        _header = header
        temp = []
        temp = kkma.morphs(_header)
        temp = [word for word in temp if not word in stopwords]
        toEmotion.append(temp)

        temp2 = []
        #logic 1 - nouns extract
        # temp2 = kkma.nouns(_header) 
        # temp2 = [word2 for word2 in temp2 if not word2 in stopwords]
        # logic 2 - simple split
        temp2 = _header.split(" ")
        temp2 = [word2 for word2 in temp2 if not word2 in stopwords]
        toFrequency.append(temp2)
    sec = time.time() - start

    Q.put(toEmotion)
    Q.put(toFrequency)
    Q.put(datetime.timedelta(seconds=sec))
    


def frequencyAnalysis(data: list, query: str) -> list:
    start = time.time()
    result = {}
    for row in data:
        for word in row:
            if result.get(word) == None:
                result[word] = 1
            else: 
                result[word] += 1

    if result.get(query) != None:
        del result[query]

    sortDict = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    sec = time.time() - start
    Q.put(list(sortDict.keys())[:30])
    Q.put(list(sortDict.values())[:30])
    Q.put(datetime.timedelta(seconds=sec))


def EmotionAnalysisByPredictor(data: list) -> list:
    start = time.time()
    with open("./model/tokenizer.pickle",'rb') as handle:
        tokenizer = pickle.load(handle)

    tokenizer.fit_on_texts(data) 
    __titles = tokenizer.texts_to_sequences(data)
    trained_model = tf.keras.models.load_model('./model/posneg_model.h5')
    max_len = 20
    data_s = pad_sequences(__titles, maxlen=max_len)
    predict = trained_model.predict(data_s)
    predict_labels = np.argmax(predict, axis=1)

    count_vec = [0, 0, 0]
    __tmp = predict_labels.tolist()
    for i in __tmp:
        if i == 0: #부정
            count_vec[0] += 1
        elif i == 1:  #중립
            count_vec[1] += 1
        else: #긍정
            count_vec[2] += 1

    sec = time.time() - start
    Q.put(data)
    Q.put(count_vec)
    Q.put(datetime.timedelta(seconds=sec))


@app.route('/api/getResult') # 접속하는 url
def index():
    start = time.time()
    q = request.args.get("query")

    pool = Pool(processes=4)
    pool.map(Crawler, (q))
    titles = Q.get()
    top10title = Q.get()
    top10href = Q.get()
    time_crawling = Q.get()

    pool.map(Tokenizer, (titles))
    toE = Q.get()
    toF = Q.get()
    time_tokenizing = Q.get()

    pool.apply(frequencyAnalysis, (toF, q,))
    word = Q.get()
    count = Q.get()
    time_fa = Q.get()

    pool.map(EmotionAnalysisByPredictor(toE))
    data = Q.get()
    predict_val = Q.get()
    time_ep = Q.get()

    pool.close()
    pool.join()

    sec = time.time() - start

    return jsonify(
        running_time=str(datetime.timedelta(seconds=sec)),
        time_crawling=str(time_crawling),
        time_tokenizing=str(time_tokenizing),
        time_fa=str(time_fa),
        time_ep=str(time_ep),
        words=word,
        counts=count,
        percentage=predict_val,
        news_header=top10title,
        news_link=top10href
    )

if __name__=="__main__":
  app.run(host="127.0.0.1", port=80)