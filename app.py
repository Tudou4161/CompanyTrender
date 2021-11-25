# app.py
from flask import Flask, render_template, jsonify, request
from source.tools import FunctionPackage
#Flask 객체 인스턴스 생성
app = Flask(__name__)


@app.route('/api/getResult') # 접속하는 url
def index():
    q = request.args.get("query")

    f = FunctionPackage(q, 20)
    results = f.__mainFunc__()

    return jsonify(
        total_time=str(results[0]),
        crawl_time=str(results[1][0]),
        token_time=str(results[1][1]),
        freq_time=str(results[1][-2]),
        emotion_time=str(results[1][-1]),
        words=results[3],
        counts=results[4],
        percentage=results[-1],
        news_header=results[2][:10],
        news_link=results[-1],
    )

if __name__=="__main__":
  app.run(host="127.0.0.1", port=80)