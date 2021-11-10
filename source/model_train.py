from keras.layers import Embedding, Dense, LSTM 
from keras.models import Sequential 
from keras.preprocessing.sequence import pad_sequences 
import pickle
from konlpy.tag import Okt 
from keras.preprocessing.text import Tokenizer 
import numpy as np 
import pandas as pd
import tensorflow as tf
from requests import NullHandler

class MyTrainModel:
    def __init__(self, trainData, testData):
        self.trainData = trainData
        self.testData = testData
        self.stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
        self.max_words = 35000
        self.max_len = 20
        self.file_name = "posneg_model.h5"
        self.x_train = None
        self.Y_train = None
        self.x_test = None
        self.Y_test = None
        self.model = None

    def morphs_tokenizer(self):
        okt = Okt()
        X_train = [] 
        for sentence in self.trainData['title']: 
            temp_X = [] 
            temp_X = okt.morphs(sentence, stem=True) # 토큰화 
            temp_X = [word for word in temp_X if not word in self.stopwords] # 불용어 제거 
            X_train.append(temp_X)
            self.x_train = X_train 

        X_test = [] 
        for sentence in self.testData['title']: 
            temp_X = []
            temp_X = okt.morphs(sentence, stem=True) # 토큰화 
            temp_X = [word for word in temp_X if not word in self.stopwords] # 불용어 제거 
            X_test.append(temp_X)
            self.x_test = X_test

    def numericEncoder(self):
        tokenizer = Tokenizer(num_words = self.max_words) 
        tokenizer.fit_on_texts(self.x_train) 
        self.x_train = tokenizer.texts_to_sequences(self.x_train)
        self.x_test = tokenizer.texts_to_sequences(self.x_test)

        with open('tokenizer.pickle', 'wb') as handle:
            pickle.dump(tokenizer, handle, protocol = pickle.HIGHEST_PROTOCOL)

    def oneHotEncoder(self):
        y_train = [] 
        y_test = [] 
        for i in range(len(self.trainData['label'])): 
            if self.trainData['label'].iloc[i] == 1: #긍정
                y_train.append([0, 0, 1]) 
            elif self.trainData['label'].iloc[i] == 0: #중립
                y_train.append([0, 1, 0])  
            elif self.trainData['label'].iloc[i] == -1: #부정 
                y_train.append([1, 0, 0]) 

        for i in range(len(self.testData['label'])): 
            if self.testData['label'].iloc[i] == 1: 
                y_test.append([0, 0, 1]) 
            elif self.testData['label'].iloc[i] == 0: 
                y_test.append([0, 1, 0]) 
            elif self.testData['label'].iloc[i] == -1: 
                y_test.append([1, 0, 0]) 

        self.Y_train = np.array(y_train) 
        self.Y_test = np.array(y_test)

    def padSequences(self):
        self.x_train = pad_sequences(self.x_train, maxlen=self.max_len)
        self.x_test = pad_sequences(self.x_test, maxlen=self.max_len)

    def modelTrainer(self): 
        model = Sequential() 

        model.add(Embedding(self.max_words, 100)) 
        model.add(LSTM(128)) 
        model.add(Dense(3, activation='softmax')) 
        model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy']) 
        history = model.fit(self.x_train, self.Y_train, epochs=10, batch_size=10, validation_split=0.2)

        model.save("posneg_model.h5")

        self.model = model

    def predictor(self):
        predict = self.model.predict(self.x_test)
        predict_labels = np.argmax(predict, axis=1)
        origin_labels = np.argmax(self.Y_test, axis=1)
        for i in range(30): 
            print("기사제목 : ", self.testData['title'].iloc[i], "/\t 원래 라벨 : ", origin_labels[i], "/\t예측한 라벨 : ", predict_labels[i])
            
    def __executor__(self):
        self.morphs_tokenizer()
        self.numericEncoder()
        self.oneHotEncoder()
        self.padSequences()
        self.modelTrainer()
        self.predictor()


if __name__ == "__main__":
    train_data = pd.read_csv("./train_dataset_1007.csv") 
    test_data = pd.read_csv("./test_dataset_1007.csv")

    model = MyTrainModel(train_data, test_data)
    model.__executor__()