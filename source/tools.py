from keras.preprocessing.sequence import pad_sequences
import requests 
from bs4 import BeautifulSoup as bs
import re 
import pandas as pd 
from tqdm import tqdm
from konlpy.tag import Kkma 
import numpy as np
import pickle
import tensorflow as tf
import time
import datetime


def Crawler(query: str) -> list:
    start = time.time()
    __titles = []
    for page in range(3): 
        raw = requests.get('https://search.naver.com/search.naver?&where=news&query=' + query + '&start=' + str((page*10)+1)).text 
        html = bs(raw, 'html.parser') 
        titles = html.select('a.news_tit') 
        for title in titles: 
            header = title.text
            clean_title = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', header)
            __titles.append(clean_title)
    sec = time.time() - start
    return __titles, datetime.timedelta(seconds=sec)

def Tokenizer(headers: list) -> list:
    start = time.time()
    toEmotion, toFrequency = [], []
    stopwords = ['의', '가', '이', '은', '들', '를', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
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
        #logic 2 - simple split
        temp2 = _header.split(" ")
        temp2 = [word2 for word2 in temp2 if not word2 in stopwords]
        toFrequency.append(temp2)
    sec = time.time() - start
    return toEmotion, toFrequency, datetime.timedelta(seconds=sec)


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
    return list(sortDict.keys()), list(sortDict.values()), datetime.timedelta(seconds=sec)

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

    sec = time.time() - start
    return data, predict_labels.tolist(), datetime.timedelta(seconds=sec)