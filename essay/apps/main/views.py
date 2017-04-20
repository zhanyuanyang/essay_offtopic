# -*- coding:utf-8 -*-
from __future__ import unicode_literals

import json
import os

from django.http import HttpResponseRedirect
from django.shortcuts import render
from algorithm.NBscore import Score as sc
from algorithm.OffTopic import Detection as de
from algorithm.check import check
from algorithm.supervised import Offtopic as offtopic
from models import Essay
from models import User
from models import User_Essay
from models import Report

global detector_un
detector_un = de.Detector("")



# 贝叶斯评分
def score(request):
    dict = {}
    text = ''
    if request.POST:
        # dict['t1']=request.POST['t1']
        content = request.POST['t2']
        test = sc.Score()
        text = [content]
        dict['score'] = test.run(text)

    return render(request, 'main/test2_score.html', dict)


# 无监督跑题检测
def detect(request):
    dict = {}

    if request.POST:
        title = request.POST['t1']
        content = request.POST['t2']
        detector = de.Detector(title)

        dict['score'] = float(detector.offtopic_detect(content, 'LDA'))

    return render(request, 'main/test1_detect.html', dict)


# 有监督跑题检测
def detect2(request):
    dict = {}
    contentwrapper = []
    if request.POST:
        # title = request.POST['t1']
        content = request.POST['t2']
        detector = offtopic.Detection(title=0)
        contentwrapper.append(content)
        result = detector.run(contentwrapper)
        # print result
        if result == 'true':
            dict['result'] = "切题"
        elif result == 'false':
            dict['result'] = "跑题"

    return render(request, 'main/test3_detect2.html', dict)


# 重定向测试
def update_time(request):
    # pass  ...   form处理
    return HttpResponseRedirect('/score')  # 跳转界面


# 日历页面显示写作页面，蓝色按钮
def write_offtopic(request):
    str_due_time = request.GET['key']
    import datetime
    re = datetime.datetime.strptime(str_due_time, "%Y-%m-%d")
    due_time = re
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    essay_object = Essay.objects.get(due_time=due_time)
    result = {}
    result['type'] = essay_object.type
    # try:

    # request.session['user_id'] = user.user_id
    if result['type'] == 'AT':
        if len(User_Essay.objects.filter(essay_id=essay_object, user_id=user)) > 0:
            record = User_Essay.objects.get(essay_id=essay_object, user_id=user)
        else:
            User_Essay.objects.create(essay_id=essay_object, user_id=user)
            record = User_Essay.objects.get(essay_id=essay_object, user_id=user)

        result['title'] = record.user_title
        result['content'] = record.content
        result['user_id'] = user.user_id
        result['record_id'] = record.id
        return render(request, 'selfWrite.html', result)
    elif result['type'] == 'PL':
        if len(User_Essay.objects.filter(essay_id=essay_object, user_id=user)) > 0:
            record = User_Essay.objects.get(essay_id=essay_object, user_id=user)
        else:
            record = User_Essay()
            record.essay_id = essay_object
            record.user_id = user
            record.user_title = essay_object.title
            record.save()

        result['title'] = record.user_title
        result['content'] = record.content
        result['user_id'] = user.user_id
        result['record_id'] = record.id

        return render(request, 'main/planWrite.html', result)
        # except:
        #     if result['type'] == 'AT':
        #         return render(request, 'selfWrite.html')
        #     elif result['type'] == 'PL':
        #         return render(request, 'planWrite.html')


# 日历页面查看结果页面，绿色按钮
def calendar_result(request):
    due_date = request.GET['key']
    import datetime
    re = datetime.datetime.strptime(due_date, "%Y-%m-%d")
    due_time = re
    essay = Essay.objects.get(due_time=due_time)
    user_id = request.session['user_id']
    user = User.objects.get(user_id=user_id)
    record = User_Essay.objects.get(essay_id=essay, user_id=user)
    if len(Report.objects.filter(essay_id=essay, user_id=user)) > 1:
        report = Report.objects.filter(essay_id=essay, user_id=user)[0]
    elif len(Report.objects.filter(essay_id=essay, user_id=user)) == 1:
        report = Report.objects.get(essay_id=essay, user_id=user)
    result = {}
    result['actual_name'] = request.session.get('actual_name')
    result['chart1'] = report.chart1
    result['chart2'] = report.chart2
    result['errors'] = report.error
    result['detail'] = report.detail
    result['score'] = report.score
    detect_result = report.isOffTopic
    result['feedback'] = report.feedback
    result['actual_name'] = request.session['actual_name']
    # 添加标题
    # TODO:修改时间0408
    # 传回标题和类型以显示
    # 无监督评分为0，传回给前端用于显示
    result['title'] = record.user_title
    if essay.type == "AT":
        result['type'] = "自主学习"
        result['score'] = 0
    elif essay.type == "PL":
        result['type'] = "计划学习"

    if detect_result == True:
        result['isOffTopic'] = "切题"
    elif detect_result == False:
        result['isOffTopic'] = "跑题"
        result['score'] = 0

    # 传入内容渲染
    dict = {}
    dict['content'] = record.content
    result['content'] = json.dumps(dict)

    return render(request, 'main/planResult.html', result)


# 无监督自选题目提交作文
def saveUnsuperviesd(request):
    result = {}
    if request.POST:
        # 获取表单
        title = request.POST['title']
        content = request.POST['content']
        sign = request.POST['sign']
        user_essay_id = request.POST['record_id']
        print '+++++++++++++++', type(user_essay_id)
        result['sign'] = sign
        # 1.session获取截止日期的任务id
        # TODO:改正
        record = User_Essay.objects.get(id=user_essay_id)
        essay = record.essay_id
        # 2.session获取用户id
        # TODO:改
        user = User.objects.get(user_id=request.session['user_id'])

        if len(User_Essay.objects.filter(user_id=user, essay_id=essay)) > 0:
            # 有就更新
            record = User_Essay.objects.get(user_id=user, essay_id=essay)
            record.content = content
            record.user_title = title
            record.save()
            # if sign == '1':
            #     return HttpResponseRedirect('/main/login_action')#*************************

        else:
            # 没有就创建
            User_Essay.objects.create(content=content, isSubmit=False, essay_id=essay, user_id=user, user_title=title)

        # 1为保存; 2 为提交
        # if sign == '1':
        #     return HttpResponseRedirect('/login_action')

        if sign == '2':
            # User_Essay.objects.create(content=content, isSubmit=True, essay_id=essay, user_id=user, user_title=title)

            # 创建结果
            result['chart1'] = json.dumps(check.getChart1(content))
            result['chart2'] = json.dumps(check.getChart2(content))
            errors, detail = check.getErrors(content)
            result['errors'] = json.dumps(errors)
            result['detail'] = json.dumps(detail)
            result['feedback'] = check.getFeedback(content)
            result['actual_name'] = request.session['actual_name']
            # 传回题目和类型
            result['title'] = title
            result['type'] = "自主学习"
            # 无监督没有评分
            result['score'] = 0
            # TODO:排名
            user.exp = user.exp + 10
            user.save()
            #
            # 检测离题
            detector_un.set_title(title)
            # detect_result=float(detector_un.offtopic_detect(content, 'LDA'))
            detect_result = float(detector_un.offtopic_detect(content, 'TextRank'))
            boolean_value = False
            if detect_result < 0.15:
                result['isOffTopic'] = "跑题"
                boolean_value = False
            else:
                result['isOffTopic'] = "切题"
                boolean_value = True

            result['score'] = 0

            Report.objects.get_or_create(user_id=user, essay_id=essay, error=result['errors'], chart1=result['chart1'],
                                         chart2=result['chart2'], detail=result['detail'], isOffTopic=boolean_value,
                                         score='no', feedback=result['feedback'])

            # 传入内容渲染
            dict = {}
            dict['content'] = record.content
            result['content'] = json.dumps(dict)

            # 更新属性
            record = User_Essay.objects.get(user_id=user, essay_id=essay)
            record.isSubmit = True
            record.save()

            return render(request, 'main/planResult.html', result)

        user = record.user_id
        # print report
        # 创建结果
        result['title'] = record.user_title
        result['content'] = record.content
        result['type'] = essay.type
        result['user_id'] = user.user_id
        result['record_id'] = record.id
        request.session['user_id'] = user.user_id
        return render(request, 'main/selfWrite.html', result)


# 有监督限定标题提交作文，查看结果
def saveEssay(request):
    result = {}
    if request.POST:
        # 获取表单
        # TODO:title从数据库获取
        # title = request.POST['title']
        content = request.POST['content']
        sign = request.POST['sign']
        user_essay_id = request.POST['record_id']
        result['sign'] = sign

        # 1.session获取截止日期的任务id
        record = User_Essay.objects.get(id=user_essay_id)
        essay = record.essay_id

        # 2.session获取用户id
        user = User.objects.get(user_id=request.session['user_id'])

        if len(User_Essay.objects.filter(user_id=user, essay_id=essay)) > 0:
            # 有就更新
            record = User_Essay.objects.get(user_id=user, essay_id=essay)
            record.content = content
            # record.user_title = title
            record.save()
            # if sign == '1':
            #     return HttpResponseRedirect('/main/login_action')

            # else:
            # 没有就创建
            # User_Essay.objects.create(content=content, isSubmit=False, essay_id=essay, user_id=user, user_title=title)

        # 1为保存; 2 为提交
        # if sign == '1':
        #     #TODO:经验值
        #     return HttpResponseRedirect('/login_action')

        if sign == '2':
            # User_Essay.objects.create(content=content, isSubmit=True, essay_id=essay, user_id=user, user_title=title)

            # 创建结果
            result['chart1'] = json.dumps(check.getChart1(content))
            result['chart2'] = json.dumps(check.getChart2(content))
            errors, detail = check.getErrors(content)
            result['errors'] = json.dumps(errors)
            result['detail'] = json.dumps(detail)
            result['feedback'] = check.getFeedback(content)
            result['actual_name'] = request.session['actual_name']
            # 传回标题和类型以显示
            useressay = User_Essay.objects.filter(user_id=user, essay_id=essay)
            result['title'] = useressay.user_title
            result['type'] = "计划学习"
            # TODO:排名
            #
            # TODO:经验值
            user.exp = user.exp + 10
            user.save()
            # 评分
            if "water" in record.user_title:
                scorer = sc.Score(title=1)
            else:
                # haste waste
                scorer = sc.Score(title=0)
            result['score'] = scorer.run([content])

            # 检测离题
            if "water" in record.user_title:
                detector_su = offtopic.Detection(title=1)
            else:
                # haste waste
                detector_su = offtopic.Detection(title=0)

            # detector_su = offtopic.Detection(title=0)
            contentwrapper = []
            contentwrapper.append(content)
            detect_result = detector_su.run(contentwrapper)
            temp = False
            if detect_result == 'true':
                result['isOffTopic'] = "切题"
                temp = True
            elif detect_result == 'false':
                result['isOffTopic'] = "跑题"
                result['score'] = 0
                temp = False
            Report.objects.get_or_create(user_id=user, essay_id=essay, error=result['errors'], chart1=result['chart1'],
                                         chart2=result['chart2'], detail=result['detail'], isOffTopic=temp,
                                         score=result['score'], feedback=result['feedback'])

            print '++++++++++++++', result['score']

            # 传入内容渲染
            dict = {}
            dict['content'] = record.content
            result['content'] = json.dumps(dict)

            # 更新属性
            record = User_Essay.objects.get(user_id=user, essay_id=essay)
            record.isSubmit = True
            record.save()

            return render(request, 'planResult.html', result)

        user = record.user_id
        # print report
        # 创建结果
        result['title'] = record.user_title
        result['content'] = record.content
        result['type'] = essay.type
        result['user_id'] = user.user_id
        result['record_id'] = record.id
        request.session['user_id'] = user.user_id
        return render(request, 'main/planWrite.html', result)


# 历史页面，作文查看
def history_result(request):
    result = {}
    record = User_Essay.objects.get(id=request.GET['id'])
    essay = record.essay_id
    user = record.user_id
    report = Report.objects.get(essay_id=essay, user_id=user)
    # print report
    # 创建结果
    result['actual_name'] = request.session.get('actual_name')
    result['chart1'] = report.chart1
    result['chart2'] = report.chart2
    result['errors'] = report.error
    result['detail'] = report.detail
    result['score'] = report.score
    detect_result = report.isOffTopic
    result['feedback'] = report.feedback
    # 添加标题
    # 传回标题和类型以显示;无监督评分为0
    result['title'] = record.user_title
    selected_essay = Essay.objects.get(id=essay)
    if selected_essay.type == "AT":
        result['type'] = "自主学习"
        result['score'] = 0
    elif selected_essay.type == "PL":
        result['type'] = "计划学习"

    if detect_result == True:
        result['isOffTopic'] = "切题"
    elif detect_result == False:
        result['isOffTopic'] = "跑题"

    # 传入内容渲染
    dict = {}
    dict['content'] = record.content
    result['content'] = json.dumps(dict)

    # result['content'] = record.content
    temp = report.isOffTopic

    if temp:
        result['isOffTopic'] = "切题"
    else:
        result['isOffTopic'] = "跑题"
        result['score'] = 0

    return render(request, 'main/planResult.html', result)


# 中间结果页面
def intermediateResults(request):
    result = {}
    record = User_Essay.objects.get(id=request.GET['id'])
    essay = record.essay_id
    user = record.user_id
    report = Report.objects.get(essay_id=essay, user_id=user)
    # print report
    # 创建结果
    result['actual_name'] = request.session.get('actual_name')
    result['chart1'] = report.chart1
    result['chart2'] = report.chart2
    result['errors'] = report.error
    result['detail'] = report.detail
    result['score'] = report.score
    detect_result = report.isOffTopic
    result['feedback'] = report.feedback
    # 添加标题
    result['title'] = record.user_title;

    if detect_result == True:
        result['isOffTopic'] = "切题"
    elif detect_result == False:
        result['isOffTopic'] = "跑题"

    # 传入内容渲染
    dict = {}
    dict['content'] = record.content
    result['content'] = json.dumps(dict)

    # result['content'] = record.content
    temp = report.isOffTopic

    if temp:
        result['isOffTopic'] = "切题"
    else:
        result['isOffTopic'] = "跑题"

    return render(request, 'main/intermediateResults.html', result)


# 历史页面写作
def write_historyEssay(request):
    result = {}
    record = User_Essay.objects.get(id=request.GET['id'])
    essay = record.essay_id
    user = record.user_id
    # print report
    # 创建结果
    result['title'] = record.user_title
    result['content'] = record.content
    result['type'] = essay.type
    result['user_id'] = user.user_id
    result['record_id'] = record.id
    # request.session['user_id'] = user.user_id

    if essay.type == 'AT':
        return render(request, 'main/selfWrite.html', result)
    else:
        return render(request, 'main/planWrite.html', result)


# 登陆页面的显示
def login(request):
    return render(request, 'main/Login&Register.html')


# 注册事件响应
def register_action(request):
    user_id = request.POST.get('user_id', 'user_id')
    actual_name = request.POST.get('actual_name', 'actual_name')
    password = request.POST.get('password', 'password')
    confirm_password = request.POST.get('confirm_password', 'confirm_password')
    if password == confirm_password:
        User.objects.create(user_id=user_id, actual_name=actual_name, password=password, avatar='', exp=0)
        return render(request, 'main/Login&Register.html', {'result': 'succes'})
    else:
        return render(request, 'main/Login&Register.html', {'result': 'fail'})


# 登陆事件响应
def main(request):
    user = ''
    query = ''
    if request.session.get('user_id'):
        print request.session.get('user_id')
        query = User.objects.get(user_id=request.session.get('user_id'))
        user = User.objects.filter(user_id=query.user_id)
    else:
        USER_ID = request.POST.get('user_id')
        PASSWORD = request.POST.get('password')
        query = User.objects.get(user_id=USER_ID)
        if PASSWORD == query.password:
            request.session['user_id'] = USER_ID
            request.session['actual_name'] = query.actual_name
            # request.session['personico'] = query.avatar
            user = User.objects.filter(user_id=USER_ID)
        else:
            return render(request, 'main/Login&Register.html', {'result': 'error'})
    personico = query.avatar
    sum = User_Essay.objects.all().filter(user_id=user)
    essay = User_Essay.objects.all().values('essay_id').filter(user_id=user)
    date = []
    for i in essay:
        due_time = Essay.objects.get(id=i["essay_id"]).due_time.strftime('%Y-%m-%d')
        type = Essay.objects.get(id=i["essay_id"]).type
        submit = User_Essay.objects.get(essay_id=i["essay_id"], user_id=user).isSubmit
        list = due_time.split('-')
        dict = {}
        dict['year'] = list[0]
        dict['month'] = list[1]
        dict['day'] = list[2]
        dict['issubmit'] = submit
        dict['type'] = type
        date.append(dict)
    id = Essay.objects.all().values('id')
    essay_list = []
    for i in essay:
        essay_list.append(i['essay_id'])
    for j in id:
        if j['id'] not in essay_list:
            due_time = Essay.objects.get(id=j["id"]).due_time.strftime('%Y-%m-%d')
            type = Essay.objects.get(id=j["id"]).type
            list = due_time.split('-')
            dict = {}
            dict['year'] = list[0]
            dict['month'] = list[1]
            dict['day'] = list[2]
            dict['issubmit'] = False
            dict['type'] = type
            date.append(dict)
    print len(date)
    return render(request, 'main/calendar.html',
                  {'actual_name': request.session.get('actual_name'), 'personico': personico,
                   'exp': query.exp,
                   'written_num': len(sum), 'date': json.dumps(date)})


# 点击头像
def setting_avatar(request):
    if request.method == "POST":
        f = request.FILES.get('personico')
        baseDir = os.path.dirname(os.path.abspath(__name__))
        jpgdir = os.path.join(baseDir, 'apps', 'main', 'static', 'login', 'jpg')

        filename = os.path.join(jpgdir, f.name)
        fobj = open(filename, 'wb')
        for chrunk in f.chunks():
            fobj.write(chrunk)
        fobj.close()
        User.objects.filter(user_id=request.session.get('user_id')).update(avatar=f.name)
        return render(request, 'main/calendar.html', {'personico': f.name})
    else:
        return render(request, 'main/calendar.html')


# 历史作文页面显示
def show_history(request):
    user_id = request.session.get('user_id')
    # print userid
    # 方法一
    # b = User.objects.get(user_id=userid)
    # essaylist = b.user_essay_set.all()
    # for i in essaylist.values('content'):
    #     print i['content']
    # 方法二
    b = User.objects.get(user_id=user_id)
    result = User_Essay.objects.filter(user_id=b)
    essay_list = []
    for i in result:
        # temp = Essay.objects.filter(essay_id=i.essay_id)
        e = i.essay_id
        type = ''
        if e.type == 'PL':
            type = '计划学习'
        elif e.type == 'AT':
            type = '自主学习'

        essay_list.append([i.id, type, i.user_title, i.update_date, i.isSubmit])

    context = {'essaylist': essay_list, 'actual_name': request.session.get('actual_name')}
    # TODO：根据isSubmit的值判断操作跳转，前端部分
    return render(request, 'main/myhistory.html', context)


def exit(request):
    # request.session.set_expiry()
    del request.session['user_id']
    del request.session['actual_name']
    return render(request, 'main/Login&Register.html')

# #结果页面显示
# def show_result(request):
#
#     user_id = request.session.get('user_id')
#     user = User.objects.filter(user_id=user_id)
#     # essay =
#
#     #example
#     result ={}
#     #errors渲染前端作文错误
#     errors = [{'index':{'start':1,'end':3},'error_type':'missSpelling','replace_word':['hello','halo']}]
#     #chart1：错误类型数据渲染图表
#     chart1 = {'adj':'100','v':'200','n':'300','adv':'400'}
#     #chart2：使用词数类型数据渲染图表
#     chart2 = {'adj':'100','v':'200','n':'300','adv':'400'}
#     #detail详细错误
#     detail = [('详细错误',''),()]
#     result['errors'] = json.dumps(errors)
#     result['chart1'] = json.dumps(chart1)
#     result['chart2'] = json.dumps(chart2)
#     result['detail'] = detail
#     result['score'] = ''
#
#
#     result['isOffTopic']="离题"
#     result['rank'] = ''
#     result['total_essaynum']=''
#
#
#
#     # Report.objects.create(isOffTopic=True,Score='10',error_list=errorlist)
#     return render(request,'planResult.html',result)
