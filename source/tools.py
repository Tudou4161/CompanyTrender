import datetime
from keras.preprocessing.sequence import pad_sequences
from concurrent.futures import ThreadPoolExecutor
import requests 
from bs4 import BeautifulSoup as bs
import re 
from konlpy.tag import Komoran
import numpy as np
import pickle
import tensorflow as tf
import time as t

class FunctionPackage:

    def __init__(self, query, max_page):
        self.trained_model = tf.keras.models.load_model('./model/posneg_model.h5')
        self.query = query
        self.komoran = Komoran()
        self.threadPool = 16
        self.max_page = max_page
        self.links = []
        

    #텍스트 클렌징 함수
    def clean_str(self, text):
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

    #크롤링 함수
    def crawler(self, page):
        origin_titles = []
        raw = requests.get('https://search.naver.com/search.naver?&where=news&query=' + self.query + '&start=' + str((page*10)+1)).text 
        html = bs(raw, 'html.parser') 
        titles = html.select('a.news_tit') 
        for title in titles: 
            header = title.text
            origin_titles.append(header)
            self.links.append(title.get("href"))
        return origin_titles

    #형태소 기준 토크나이징 함수
    def morphs_token(self, header, stopwords):
        _header = self.clean_str(header)
        temp = self.komoran.morphs(_header)
        temp2 = [word for word in temp if not word in stopwords]
        return temp2
    #단순 토크나이징 함수
    def simple_token(self, header, stopwords):
        _header = self.clean_str(header)
        temp = _header.split(" ")
        temp2 = [word for word in temp if not word in stopwords]
        return temp2

    #빈도수 분석 함수
    def frequencyAnalysis(self, data):
        result = {}
        for row in data:
            for word in row:
                if result.get(word) == None:
                    result[word] = 1
                else: 
                    result[word] += 1

        copy_query = self.query
        if result.get(copy_query) != None:
            del result[copy_query]

        sortDict = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
        return list(sortDict.keys())[:30], list(sortDict.values())[:30]

    #감성분석 함수
    def EmotionAnalysisByPredictor(self, data):
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

        return count_vec

    def __mainFunc__(self):
        #1. 크롤링 멀티스레딩
        start1 = t.time()
        headers = []
        with ThreadPoolExecutor(max_workers=16) as exec:
            for one_page in exec.map(self.crawler, list(range(1, self.max_page))):
                for elem in one_page:
                    headers.append(elem)
            end1 = t.time() - start1
            print(end1)

            #2. 토크나이징 멀티스레딩        
        stopwords = ['이', '있', '하', '것', '들', '그', '되', '수', '이', '보', '않', '없', '나', 
        '사람', '주', '아니', '등', '같', '우리', '때', '년', '가', '한', '지', '대하', '오', '말', 
        '일', '그렇', '위하', '때문', '그것', '두', '말하', '알', '그러나', '받', '못하', '일', '그런', 
        '또', '문제', '더', '사회', '많', '그리고', '좋', '크', '따르', '중', '나오', '가지', '씨', '시키',
        '만들', '지금', '생각하', '그러', '속', '하나', '집', '살', '모르', '적', '월', '데', '자신', '안', 
        '어떤', '내', '내', '경우', '명', '생각', '시간', '그녀', '다시', '이런', '앞', '보이', '번', '나', '뉴', '큰', '획', '긋고'
        '다른', '어떻', '여자', '개', '전', '들', '사실', '이렇', '점', '싶', '말', '정도', '좀', '원', '잘', '통하', '소리', '놓']

        toE, toF = [], []
        start2 = t.time()
        with ThreadPoolExecutor(max_workers=16) as exec:
            for morph, simple in zip(exec.map(self.morphs_token, headers, stopwords), exec.map(self.simple_token, headers, stopwords)):
                toE.append(morph)
                toF.append(simple)
            end2 = t.time() - start2
            print(end2)

        #3. 빈도수 분석
        start3 = t.time()
        freq_labels, freq_counts = self.frequencyAnalysis(toF)
        end3 = t.time() - start3
        print(end3)

        print(toE)

        #4. 감성분석 멀티스레딩
        start4 = t.time()
        emotion_labels = self.EmotionAnalysisByPredictor(toE)
        end4 = t.time() - start4
        print(end4)

        total_time = end1 + end2 + end3 + end4

        return [total_time, [end1, end2, end3, end4], 
            headers, freq_labels, freq_counts, emotion_labels, self.links[:10]]


if __name__ == "__main__":
    f = FunctionPackage("삼성전자", 10)
    result_pack = f.__mainFunc__()
    print(datetime.timedelta(seconds=result_pack[0]))
    print(result_pack[0])

    # x = f.EmotionAnalysisByPredictor(['삼성', '더', '프레임', 'TV', '밀리언', '셀러', '등극'])
    # print(x)

