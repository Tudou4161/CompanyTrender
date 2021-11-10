# app.py
from flask import Flask, render_template, jsonify, request
from source.tools import Tokenizer, Crawler, frequencyAnalysis, EmotionAnalysisByPredictor
import time
import datetime
#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/getResult') # 접속하는 url
def index():
  start = time.time()
  q = request.args.get("query")
  titles, time_crawling = Crawler(query=q)
  toE, toF, time_tokenizing = Tokenizer(titles)
  word, count, time_fa = frequencyAnalysis(data=toF, query=q)
  data, predict_val, time_ep = EmotionAnalysisByPredictor(data=toE)
  sec = time.time() - start

  return jsonify(
    running_time=str(datetime.timedelta(seconds=sec)),
    time_crawling=str(time_crawling),
    time_tokenizing=str(time_tokenizing),
    time_fa=str(time_fa),
    time_ep=str(time_ep),
    words=word,
    counts=count,
    percentage=predict_val
  )

if __name__=="__main__":
  app.run(host="127.0.0.1", port=80)