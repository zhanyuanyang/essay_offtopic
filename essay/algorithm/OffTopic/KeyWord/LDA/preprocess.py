#-*- coding:utf-8 -*-
import numpy as np

import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')

#去停用词
def deleteStopwords(word_list,stopwords):
    finalwords = []
    for word in word_list:
        if word in stopwords:
            continue
        finalwords.append(word)
    return finalwords

#将作文转换为小写并切分成词
def article2wordlist(article):
    word_list = []
    while 1:
        line = article.readline()
        if line.strip()=='':
            break
        line = str(line)
        string = re.sub("[+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), "".decode("utf8"), line)
        string = string.encode('utf8')
        line = string.lower().split()
        for word in line:
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


if __name__ == '__main__':
    stopwords = open('preprocess/stopwords.txt','r')
    article = open('data/article.txt','r')

    wordlist = article2wordlist(article)
    stopwordlist = getstopwordlist(stopwords)
    finallist = deleteStopwords(wordlist,stopwordlist)
    f = open('data/train.dat','w')
    for line in finallist:
        f.write(line)
        f.write(' ')
    stopwords.close()
    article.close()
    f.close()
    print 'PreProcess finished'

