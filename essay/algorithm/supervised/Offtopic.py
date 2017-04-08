# -*-coding:utf-8 -*-
from sklearn.externals import joblib
import os

class Detection:
    def __init__(self,title=0):
        self.title = title
        self.target_names = ['false','true']

    def GlobalWater(self,text):
        countVec = joblib.load(os.getcwd()+'/algorithm/supervised/GWdetection_count.pkl')
        Tfidf = joblib.load(os.getcwd()+'/algorithm/supervised/GWdetection_tfidf.pkl')
        Model = joblib.load(os.getcwd()+'/algorithm/supervised/GWdetection_model.pkl')
        x_count = countVec.transform(text)
        x_tfidf = Tfidf.transform(x_count)
        predict = Model.predict(x_tfidf)
        return self.target_names[int(predict)]

    def HasteWaste(self,text):
        countVec = joblib.load(os.getcwd()+'/algorithm/supervised/HWdetection_count.pkl')
        Tfidf = joblib.load(os.getcwd()+'/algorithm/supervised/HWdetection_tfidf.pkl')
        Model = joblib.load(os.getcwd()+'/algorithm/supervised/HWdetection_model.pkl')
        x_count = countVec.transform(text)
        x_tfidf = Tfidf.transform(x_count)
        predict = Model.predict(x_tfidf)
        return self.target_names[int(predict)]

    def __del__(self):
        print "Detection instance has been deleted!"

    def run(self,text):
        if self.title == 1:
            result = self.GlobalWater(text)
            return result
        if self.title == 0:
            result = self.HasteWaste(text)
            return result

if __name__ == '__main__':
    test = Detection(title=1)
    text = ["In my daily life, I always want things to be done quickly, however, the results tend to turn out just the opposite of what I wish. As the saying goes “more haste, less speed”, baste never helps, instead it makes waste. Once I was in a hurry trying to catch the train to Shanghai. I packed up and put all the things I would need into a suitcase and locked it. Then I took a taxi and boarded the train on time. When I arrived in Shanghai and was comfortably settled in a hotel, I tried to open my suitcase. To my great disappointment, I found I did not have the key with me. I had left it at home without my knowing it. Another Time I was trying to fill a bettIe with hot water to warm my feet before going to bed. In a hurry, I took the bottle full of “cold water” and poured it out. While I was pouring and cnjoying the sound the liquid made while coming out of the bottle, my brother shouted at me, “Hey, you are pouring out my liqor!” From my own experinece, I draw a painful lesson HASTE MAKES WASTE."]

    print test.run(text)
