# -*- coding:utf-8 -*-
from sklearn.externals import joblib
import os

class Score:
    def __init__(self,title=0):
        self.title = title
        self.target_names = ['a','b','c']
    def run(self,text):
        if self.title == 1:
            result = self.GlobalWater(text)
            return result
        elif self.title == 0:
            result = self.HasteWaste(text)
            return result


    def GlobalWater(self,text):
        countVec = joblib.load(os.getcwd()+'/algorithm/NBscore/GWscore_count.pkl')
        Tfidf = joblib.load(os.getcwd()+'/algorithm/NBscore/GWscore_tfidf.pkl')
        Model = joblib.load(os.getcwd()+'/algorithm/NBscore/GWscore_model.pkl')
        x_count = countVec.transform(text)
        x_tfidf = Tfidf.transform(x_count)
        predict = Model.predict(x_tfidf)
        return self.target_names[int(predict)]

    def HasteWaste(self,text):
        countVec = joblib.load(os.getcwd()+'/algorithm/NBscore/HWscore_count.pkl')
        Tfidf = joblib.load(os.getcwd()+'/algorithm/NBscore/HWscore_tfidf.pkl')
        Model = joblib.load(os.getcwd()+'/algorithm/NBscore/HWscore_model.pkl')
        x_count = countVec.transform(text)
        x_tfidf = Tfidf.transform(x_count)
        predict = Model.predict(x_tfidf)
        return self.target_names[int(predict)]

    def __del__(self):
        print "Score instance has been deleted!"


if __name__ == '__main__':
    # 注意 接受到的文本需以list形式传入run方法
    text1 = ["Nowadays short.  "]
    test = Score()
    print test.run(text1)
    del test

