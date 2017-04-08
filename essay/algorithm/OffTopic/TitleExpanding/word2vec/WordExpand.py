#-*- coding:utf-8 -*-

import gensim
import re

#去停用词
def deleteStopwords(word_list,stopwords):
    finalwords = [word for word in word_list if word not in stopwords]
    return finalwords

#将作文转换为小写并切分成词
def article2wordlist(article):
    word_list = []
    if article.strip()=='':
        return word_list
    article = str(article)
    string = re.sub("[+\.\!\/_,$%^*(+\"\']+|[+——！，。?？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), article).encode('utf8')
    article = string.lower().split()
    for word in article:
        word_list.append(word)
    return word_list

#读取停用词词典
def getstopwordlist(stopwords):
    stopword_list = []
    lines = stopwords.readlines()
    for line in lines:
        line = line.split()
        for word in line:
            stopword_list.append(word)
    return stopword_list

#预处理题目信息
def preprocessTitle(title):

    stopwords = open('algorithm/OffTopic/KeyWord/LDA/preprocess/stopwords.txt', 'r')

    stopwordlist = getstopwordlist(stopwords)
    wordlist = article2wordlist(title)
    finallist = deleteStopwords(wordlist, stopwordlist)
    stopwords.close()

    return finallist

