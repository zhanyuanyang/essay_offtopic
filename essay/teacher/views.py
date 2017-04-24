# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from teacher.models import *
from main.models import Essay
from main.models import User_Essay
from main.models import User
from main.models import Report
from django.http import HttpResponse
import json


def test(request):
    return render(request, 'teacherPage.html')


# 登陆页面的显示
def login(request):
    return render(request, 'teacher/Login&Register.html')


# 注册事件响应
def register_action(request):
    teacher_id = request.POST.get('teacher_id')
    name = request.POST.get('name')
    password = request.POST.get('password')
    confirm_password = request.POST.get('confirm_password')
    if password == confirm_password:
        Teacher.objects.create(teacher_id=teacher_id, name=name, password=password, avatar='')
        return render(request, 'teacher/Login&Register.html', {'result': 'succes'})
    else:
        return render(request, 'teacher/Login&Register.html', {'result': 'fail'})


def main(request):
    user = ''
    query = ''
    if request.session.get('teacher_id') and request.session.get('id'):
        query = Teacher.objects.get(teacher_id=request.session.get('teacher_id'))
    else:
        Teacher_id = request.POST.get('teacher_id')
        PASSWORD = request.POST.get('password')
        query = Teacher.objects.get(teacher_id=Teacher_id)
        if PASSWORD == query.password:
            request.session['name'] = query.name
            request.session['teacher_id'] = query.teacher_id
            request.session['id'] = query.id
        else:
            return render(request, 'Login&Register.html', {'result': 'error'})
    result = {}
    result['personico'] = query.avatar
    result['name'] = query.name
    trainedTopics_list = TrainedTopics.objects.all()
    result['trainedTopics_list'] = trainedTopics_list

    # 4.23新增：任务列表信息。完成人数-finish，题目title，截止时间duetime，文章id--essay_id
    # 学生人数
    std_num = len(User.objects.filter(teacher_id=query))
    essay_object = Essay.objects.filter(teacher_id=query)
    essayList = []
    for i in essay_object:
        temp = {}
        temp['title'] = i.title
        temp['due_time'] = i.due_time
        temp['essayid'] = i.id
        finish_num = 0
        set = User_Essay.objects.filter(essay_id=i)
        for j in set:
            if j.isSubmit == True:
                finish_num = finish_num + 1
        tempstr = str(finish_num) + "/" + str(std_num)
        temp['finish'] = tempstr
        essayList.append(temp)
    result['essayList'] = essayList
    return render(request, 'teacher/teacherPage.html', result)


# 发布作文
def essayRelease(request):
    type = request.POST.get('type')
    title = request.POST.get('title')
    description = request.POST.get('description')
    due_time = request.POST.get('due_time')
    print request.session.get('id')
    Essay.objects.create(teacher_id_id=request.session.get('id'), title=title, due_time=due_time,
                         description=description, type=type)
    query = Teacher.objects.get(teacher_id=request.session.get('teacher_id'))
    result = {}
    result['personico'] = query.avatar
    result['name'] = query.name
    trainedTopics_list = TrainedTopics.objects.all()
    return render(request, 'teacher/teacherPage.html', {'result': result, 'trainedTopics_list': trainedTopics_list})


# 查看学生的具体完成情况
# TODO:查看页面构思，最先做这个
def view(request):
    id = request.GET['id']
    teacher_id = request.session.get('teacher_id')
    query = Teacher.objects.get(teacher_id=teacher_id)
    student = User.objects.filter(teacher_id=query)
    # 显示选的是哪篇作文
    result = {}
    std_num = len(student)
    essay_object = Essay.objects.filter(teacher_id=query)
    essay = []
    for i in essay_object:
        if i.id == int(id):
            temp = {}
            temp['title'] = i.title
            temp['due_time'] = i.due_time
            temp['essayid'] = i.id
            finish_num = 0
            set = User_Essay.objects.filter(essay_id=i)
            for j in set:
                if j.isSubmit == True:
                    finish_num = finish_num + 1
            tempstr = str(finish_num) + "/" + str(std_num)
            temp['finish'] = tempstr
            essay.append(temp)
            break
    result['essay'] = essay
    # 显示学生列表
    studentList = []
    for i in student:
        temp = {}
        temp['student_id'] = i.user_id
        temp['name'] = i.actual_name
        studentList.append(temp)
    result['studentList'] = studentList
    result['id'] = id
    return render(request, 'teacher/test.html', result)


# 查看学生具体的一篇作文结果
def student_result(request):
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


# 学生管理
def std_manage(request):
    teacher_id = request.session.get('teacher_id')
    query = Teacher.objects.get(teacher_id=teacher_id)
    student = User.objects.filter(teacher_id=query)
    studentList = []
    result = {}
    for i in student:
        temp = {}
        temp['student_id'] = i.user_id
        temp['name'] = i.actual_name
        studentList.append(temp)
    result['studentList'] = studentList
    return render(request, 'teacher/studentManage.html', result)


def student_essay(request):
    student_id = request.GET['student_id']
    essayList = User_Essay.objects.filter(user_id=student_id)
    return render(request, 'teacher/student_essay.html', essayList)

# 个人信息管理，改密码之类的
def show_profile(request):
    return


def exit(request):
    del request.session['teacher_id']
    del request.session['name']
    return render(request, 'teacher/Login&Register.html')
