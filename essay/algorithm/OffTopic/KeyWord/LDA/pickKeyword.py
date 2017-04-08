#-*- coding:utf-8 -*-
from preprocess import *
import lda2


#提取关键词
def getKeywords(themePath,theme_word_path,keywords_path):
    #计算主题下抽取的词数
    f1 = open(themePath,'r')
    line1 = f1.readlines()
    theme = line1[0].strip().split()
    themenumb = len(theme)

    #这里设置LDA提取关键词的数量，现在是设置了30个，把for循环里所有的3改成2即提取20个关键词
    for n in range(0,themenumb):
        if (float(theme[n])*300%30)>5:
           theme[n] = int(float(theme[n])*30)+1
        else:
            theme[n] = int(float(theme[n])*30)
    # print theme

    #存储各类别下词语
    f2 = open(theme_word_path,'r')
    classes = []
    numb = -1
    topic = []

    for i in f2.readlines():
        if "第" in i:
            numb = numb + 1
            if numb != 0:
                classes.append(topic)
            topic = []
        else:
           topic.append(i.strip().split())
    classes.append(topic)

    #根据各个类别提取词语
    result = []

    flag1 = 0
    words = [] #存放已经抽取出的词，防止重复
    for i in range(0,themenumb):
        #在主题i下抽取词(theme[i]个)
        for y in range(0,theme[i]):
            flag = 0
            themeword = classes[i]
            if y >= len(themeword):
                break
            # print '??','y: ',y,'  ','flag: ',flag,'  ',int(y+flag),'  ',len(themeword)
            while themeword[y + flag][0] in words:#here!
                flag = flag + 1
                if (y+flag) >= len(themeword)-1:
                    flag1 = 1
                    break
            if flag1 == 1:
                break
            result.append(themeword[y + flag])
            words.append(themeword[y + flag][0])

    #排序
    for i in range(0,len(result)):
        w = result[i][0]
        freq = result[i][1]
        result[i][0] = freq
        result[i][1] = w
    result.sort()
    # print main

    #存入result.txt
    f=open(keywords_path,'w')
    for line in result:
        f.write(str(line))
        f.write('\n')
    f.close()
    return result

def getKeyword_list(keywords):
    keyword_list = []
    for i in keywords:
        keyword_list.append(i[1])
    return  keyword_list

def runLDA():
    dpre = lda2.preprocessing()
    lda = lda2.LDAModel(dpre)
    lda.est()






