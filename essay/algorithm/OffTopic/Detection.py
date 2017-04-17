# -*- coding: utf-8 -*-

import gensim
import time
import sys
import os
sys.path.append('..')
import KeyWord.LDA.pickKeyword

from TitleExpanding.word2vec.WordExpand import *
from KeyWord.TextRank4ZH.textrank4zh import TextRank4Keyword, TextRank4Sentence


class Detector:
    # model = gensim.models.Word2Vec.load_word2vec_format("algorithm/OffTopic/TitleExpanding/word2vec/wiki.en.text_50.vector", binary=False)
    def __init__(self,title):
        self.title = title
        #载入模型
        # self.model = gensim.models.Word2Vec.load_word2vec_format("algorithm/OffTopic/TitleExpanding/word2vec/wiki.en.text_50.vector", binary=False)
        print 'model loaded!'
        # 预处理题目
        self.title_list = preprocessTitle(self.title)
        print 'Title PreProcess finished'
        print 'title: ', self.title_list
        # 扩展题目信息
        self.title_expandlist = self.wordExpand()
        print 'Title Expanding finished'
        print 'Title Expanded words:  ', self.title_expandlist
        print '-------------------------'
        # 读取停用词表
        stopwords = open('algorithm/OffTopic/KeyWord/LDA/preprocess/stopwords.txt', 'r')
        self.stopwordlist = getstopwordlist(stopwords)

    @property
    def title(self):
        return self.title

    def set_title(self, title):
        self.title = title
        # 预处理题目
        self.title_list = preprocessTitle(self.title)
        print 'Title PreProcess finished'
        print 'title: ', self.title_list
        # 扩展题目信息
        self.title_expandlist = self.wordExpand()
        print 'Title Expanding finished'
        print 'Title Expanded words:  ', self.title_expandlist
        print '-------------------------'

    def getSimilarity(self,articlelist):
        similarity = 0

        #计算待测文本与题目相关度
        for titleword in self.title_expandlist:
            # 计算待测文本与各个主题词的相关度
            sim_article_titleword = 0
            for articleword in articlelist:
                try:
                    sim_article_titleword += self.model.similarity(articleword,titleword)
                except:
                    continue
            sim_article_titleword = sim_article_titleword/len(articlelist)
            similarity += sim_article_titleword

        similarity = similarity/len(self.title_expandlist)

        return similarity

    # 扩展题目信息
    def wordExpand(self):
        result = []
        for expandword in self.title_list:
            expandWords = self.model.most_similar(expandword)
            for word in expandWords:
                result.append(word[0])
        return result

    def LDA_keyword(self):
        KeyWord.LDA.pickKeyword.runLDA()
        # 提取关键词（LDA）
        # LDA提取关键词的数量在pickKeyword.py里设置！！
        themePath = 'algorithm/OffTopic/KeyWord/LDA/data/tmp/model_theta.dat'
        theme_word_path = 'algorithm/OffTopic/KeyWord/LDA/data/tmp/model_twords.dat'
        keywords_path = 'algorithm/OffTopic/KeyWord/LDA/data/tmp/main.txt'
        keywords = KeyWord.LDA.pickKeyword.getKeywords(themePath, theme_word_path, keywords_path)  # here!
        keyword_list = KeyWord.LDA.pickKeyword.getKeyword_list(keywords)
        return keyword_list
    def TextRank_keyword(self,article):
        # 提取关键词（TextRank）
        tr4w = TextRank4Keyword()
        tr4w.analyze(text=article, lower=True,
                     window=2)  # py2中text必须是utf8编码的str或者unicode对象，py3中必须是utf8编码的bytes或者str对象
        keyword_list = []
        # print('关键词：')
        # 这里设置提取的关键词数量，现在设置为30个
        for item in tr4w.get_keywords(30, word_min_len=1):
            keyword_list.append(item.word)
            # print(item.word, item.weight)
        print 'keywords: ', keyword_list
        print '-------------------------'
        return keyword_list

    def offtopic_detect(self,article,method):
        start = time.clock()

        #预处理 Article
        wordlist = article2wordlist(article)
        finallist = deleteStopwords(wordlist, self.stopwordlist)
        distinctWord = []
        for word in finallist:
            if word not in distinctWord:
                distinctWord.append(word)
        if len(distinctWord)< 30:
            print 'the article is wrongful article.!'
            return 0.0
        else:
            # print '::::::::::::::::::::::::::::::::::',os.getcwd()
            # path1=os.getcwd()+"/algorithm/OffTopic/KeyWord/LDA/data/train.dat"
            f = open(os.getcwd()+"/algorithm/OffTopic/KeyWord/LDA/data/train.dat", 'w')
            for line in distinctWord:
                f.write(line)
                f.write(' ')
            f.close()
            print 'PreProcess finished'

            if method == 'LDA':
                keyword_list = self.LDA_keyword()
                print 'keywords: ', keyword_list
                print '-------------------------'
                #计算相关度
                similarity = self.getSimilarity(keyword_list)
                end = time.clock()
                print 'Run time:',(end-start)
                print 'similarity=',similarity
            elif method == 'TextRank':
                keyword_list = self.TextRank_keyword(article)
                # 计算相关度
                similarity = self.getSimilarity(keyword_list)
                end = time.clock()
                print 'Run time:', (end - start)
                print 'similarity=', similarity
        return similarity

if __name__ == '__main__':
    title = 'global shortage of fresh water'
    article1 = "Fresh water is indispensable to the dialy live of mankind. People ever thought fresh water is countless, it may come from many sources, such as rain, river, well. . . We may use it as much as we want to. Is it really so? It has proved that we were wrong. In fact, fresh water is very short, especially now. During these years, population increased fastly , more and more fresh water are needed. Also the developing industry makes a great demand for it. Worst of all, plenty of fresh water is being polluted. Man is in short of fresh water. Since fresh water is limited and short , it's high time that we did what we can to avoid the crisis. We should take effective steps to avoid waster . Meanwhile, we should establish laws to stop pollution, otherwise the shortage of fresh water will prevent us from developing quickly."
    detector = Detector(title)
    print detector.offtopic_detect(article1,'LDA')
    print detector.offtopic_detect(article1,'TextRank')

    article2 = "It is very necessary for our college students to learn the world outside the campus. The knowledge that we can learn from the text is limited. In order to get more knowledge and work better, we have to know the world outside the campus. There are many ways to get to know the world. For example. We can know the world events by watching TV or reading newspaper. We can also go out of the campus and act in a position ourselves. such as delivering newspapers. it is a good job to a college students . and we can practise ourselves by working. I'm a normal university student. So acting as a family teacher is suitable for me. It is the best way that I can get to know the world outside the campus. I can work in my spare time and be prepared for tomorrow. "
    # print detector.offtopic_detect(article2,'LDA')
    print detector.offtopic_detect(article2,'TextRank')

    title2 = 'student college'
    print 'title',detector.title
    print 'title_list',detector.title_list
    print 'title expand list',detector.title_expandlist
    detector.set_title(title2)
    print 'title',detector.title
    print 'title_list',detector.title_list
    print 'title expand list',detector.title_expandlist

    # print detector.offtopic_detect(article1,'LDA')
    print detector.offtopic_detect(article1,'TextRank')
    # print type(os.getcwd())





