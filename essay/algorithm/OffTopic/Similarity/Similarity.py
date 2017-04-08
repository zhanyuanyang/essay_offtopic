# -*- coding: utf-8 -*-

import gensim
import time
import sys
sys.path.append('..')
import algorithm.OffTopic.KeyWord.LDA.pickKeyword
from algorithm.OffTopic.TitleExpanding.word2vec.WordExpand import *

#计算相关度
def getSimilarity(articlelist,titlelist,model):
    similarity = 0

    #计算待测文本与题目相关度
    for titleword in titlelist:
        # 计算待测文本与各个主题词的相关度
        sim_article_titleword = 0
        for articleword in articlelist:
            sim_article_titleword += model.similarity(articleword,titleword)
        sim_article_titleword = sim_article_titleword/len(articlelist)
        similarity += sim_article_titleword

    similarity = similarity/len(titlelist)

    return similarity



