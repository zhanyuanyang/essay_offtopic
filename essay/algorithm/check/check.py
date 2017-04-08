#coding=utf-8
import nltk
import language_check
from string import punctuation
from nltk.tokenize import word_tokenize
import os


# language_check

#读取pos字典
def loadPosDict(dictPath):
    posDict = {}
    pos_all = []
    file = open(dictPath,'r')
    while 1:
        line = file.readline()
        if not line:
            break
        lines = line.split()
        posDict[lines[0]] = lines[1]
        pos_all.append(lines[0])

    return posDict,pos_all



# 作用：获取图表二，词汇类型表的数据
# 传入参数为一篇文章
def getChart2(text):

    #简易词性表
    posDict,pos_all = loadPosDict(os.getcwd()+'/algorithm/check/posDict_min.txt')
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_tokenized = [word for word in word_tokenize(text.decode('utf-8'))]
    texts_filtered = [word for word in texts_tokenized if not word in english_punctuations]
    #@poslist：每个词对应的词性
    poslist = nltk.pos_tag(texts_filtered)
    # print poslist

    # for key in posDict:
    #     print key,':',posDict[key]

    #所有词类型
    chart2 = {}
    #动词类型
    verbtype = ['VB','VBG','VBD','VBN','VBP','VBZ']
    #名词类型
    nountype = ['NN','NNS','NNP','NNPS']
    #副词类型
    advtype = ['RB','RBR','RBS']
    #形容词类型
    adjtype = ['JJ','JJR','JJS']
    #句子复杂度类型,CC-连词,WP-代词,WDT-限定词,WP$-WH代词所有格,WRB-WH副词
    complextype = ['CC','WP','WDT','WP$','WRB']
    #图表二目标类型,MD-情态动词,IN-介词
    targettype = ['MD','IN']
    targettype.extend(verbtype)
    targettype.extend(nountype)
    targettype.extend(advtype)
    targettype.extend(adjtype)
    for token in poslist:
        pos = token[1]
        # print type(pos)
        if pos in targettype:
            postype = posDict.get(pos)
            # print postype
            if chart2.has_key(postype):
                chart2[postype] += 1
            else:
                chart2[postype] = 1
        elif chart2.has_key('其他') :
            chart2['其他'] += 1
        else:
            chart2['其他'] = 1

    return chart2


#作用：获得整篇文章的错误列表
#返回：返回一个错误列表@errors和一个详细错误@errors
def getErrors(text):
    # @errors:错误列表
    errors = []
    # @detail:详细错误
    detail = []

    text = text.replace('\n','')
    print text
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    # posDict_detail, pos_all_detail = loadPosDict(os.getcwd()+"/posDict_min.txt")
    posDict_detail, pos_all_detail = loadPosDict(os.getcwd() + "/algorithm/check/posDict_min.txt")
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    # print matches
    # print "错误数量有 %s 个:" % len(matches)
    for word in matches:
        fpos = word.fromx
        epos = word.tox
        # 加入errors

        # print "-------------"
        #判断有无替代词
        if len(word.replacements) > 0:
            replaceword_pos = nltk.pos_tag([word.replacements[0]])
            posWord = str(replaceword_pos[0][1].encode('utf-8'))
                # print posWord
            if posWord in english_punctuations:
                break
            replace_word = word.replacements
            error = {'index': {'start': fpos, 'end': epos}, 'error_type': posDict_detail[posWord],'replace_word': replace_word}
            errors.append(error)
        else :
            error = {'index': {'start': fpos, 'end': epos}, 'error_type': word.msg,'replace_word': replace_word}
            errors.append(error)
        error_detail = {'位置':word.context , '提示':word.msg}
        detail.append(error_detail)

    for i in detail:
        print i
    print errors
    print detail

    return errors,detail


# 作用：获取图表一，错误类型表的数据
# 传入参数为一篇文章
def getChart1(text):

    # chart1 = {'动词': 0, '名词': 0, '形容词': 0, '副词': 0, '介词': 0, '情态动词': 0}
    chart1 = {}
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    posDict_detail, pos_all_detail = loadPosDict(os.getcwd()+"/algorithm/check/posDict_min.txt")

    # 动词类型
    verbtype = ['VB', 'VBG', 'VBD', 'VBN', 'VBP', 'VBZ']
    # 名词类型
    nountype = ['NN', 'NNS', 'NNP', 'NNPS']
    # 副词类型
    advtype = ['RB', 'RBR', 'RBS']
    # 形容词类型
    adjtype = ['JJ', 'JJR', 'JJS']
    # 图表二目标类型,MD-情态动词,IN-介词
    targettype = ['MD', 'IN']
    targettype.extend(verbtype)
    targettype.extend(nountype)
    targettype.extend(advtype)
    targettype.extend(adjtype)
    # print matches
    correct_word = []

    for word in matches:
        if len(word.replacements) > 0:
            correct_word.append(word.replacements[0])
        else:
            pass


    # print correct_word

    poslist = nltk.pos_tag(correct_word)
    # print poslist

    for token in poslist:
        pos = token[1]
        # print type(pos)
        if pos in targettype:
            postype = posDict_detail.get(pos)
            # print postype
            if chart1.has_key(postype):
                chart1[postype] += 1
            else:
                chart1[postype] = 1
        elif chart1.has_key('其他') :
            chart1['其他'] += 1
        else:
            chart1['其他'] = 1

    # for key in chart1:
    #     print key,":",chart1[key]

    #补全数据
    targetKey = ['动词','名词','形容词','副词','介词','情态动词','其他']
    for i in targetKey:
        if chart1.has_key(i):
            continue
        else:
            chart1[i] = 0


    return chart1


def getFeedback(text):
    # @feedback:错误列表
    complexword = {}
    print text
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(text)
    # posDict_detail, pos_all_detail = loadPosDict(os.getcwd()+"/complextype.txt")
    posDict_detail, pos_all_detail = loadPosDict(os.getcwd() + "/algorithm/check/complextype.txt")


    for i in posDict_detail:
        print i

    correct_word =[]

    # for i in texts_filtered:
    #     print i
    print text
    #用一个临时变量，原来的text不能更改
    temp = text
    for word in matches:
        # if len(word.replacements) > 0:
        #     correct_word.append(word.replacements[0])
        a = word.fromx
        b = word.tox

        str1 =  text[a:b]
        if len(word.replacements) > 0:
            str2 = str(word.replacements[0])
            text1 = temp.replace(str1, str2)
            temp = text1;
        else:
            continue
        #text1:每次的新变量



        # print text.find(start=a,end=b)
        # print word
    print "新的：",text1


    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    texts_tokenized = [word for word in word_tokenize(text1.decode('utf-8'))]
    texts_filtered = [word for word in texts_tokenized if not word in english_punctuations]

    # 句子复杂度类型,CC-连词,WP-代词,WDT-限定词,WP$-WH代词所有格,WRB-WH副词
    complextype = ['CC', 'WP', 'WDT', 'WP$', 'WRB', 'IN']

    poslist = nltk.pos_tag(texts_filtered)
    # print poslist

    for token in poslist:
        pos = token[1]
        # print type(pos)
        if pos in complextype:
            postype = posDict_detail.get(pos)
            # print postype
            if complexword.has_key(postype):
                complexword[postype] += 1
            else:
                complexword[postype] = 1
    sum = 0
    for key in complexword:
        print key,":",complexword[key]
        sum = sum + complexword[key]
    print sum

    print len(texts_filtered)
    percent = float(sum)/len(texts_filtered)
    print percent
    if sum < 0.13:
        feedback = "结构比较简单,从句数量较少。"
    else:
        feedback = "文章层次分明，句子结构高级。"

    # feedback = ""
    return feedback

if __name__ == '__main__':
    # getChart1("we go to the smae school.She is a nice gril and helps me solve all kinds of probleem.")
    # getErrors("This is a new story of my lifee todays. Some pepple likes doing homeworrk. I don't like this. todya is cool . tomorrow will be better . ")
    # getChart2("I  have many friends, but I like Lily the most. She lives next to me, and we go to the smae school. She is a nice gril and helps me solve all kinds of probleem. I really want to return her, so when she meets difficulty, I will give my hand. I cherish our friendship so much and hope we can last it forever.")
    getFeedback("I  have many friends, but I like Lily the most. She lives next to me, and we go to the smae school. She is a nice gril and helps me solve all kinds of probleem. I really want to return her, so when she meets difficulty, I will give my hand. I cherish our friendship so much and hope we can last it forever.")