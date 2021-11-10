from source.tools import Crawler, Tokenizer, frequencyAnalysis, EmotionAnalysisByPredictor
import time 
import datetime 

if __name__ == "__main__":
    start = time.time()

    query = "두잉랩"
    titles = Crawler(query=query)
    toE, toF = Tokenizer(titles)
    result1, result2 = frequencyAnalysis(data=toF, query=query)
    # print(result)
    data, predict_val = EmotionAnalysisByPredictor(data=toE)
    # for i, j in zip(data, predict_val):
    #     print(i, j)

    sec = time.time() - start
    result = datetime.timedelta(seconds=sec)
    print(result)

    #성능체킹
    #1차시 -> 18초 621..
    #2차시(멀티 프로세싱 정의) -> 