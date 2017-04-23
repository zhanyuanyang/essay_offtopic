# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from teacher.models import *
from main.models import Essay
from main.models import User_Essay
from main.models import User
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
    if request.session.get('teacher_id'):
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

    #4.23新增：任务列表信息。完成人数-finish，题目title，截止时间duetime，文章id--essay_id
    teacher = Teacher.objects.get(id=request.session['id'])
    #学生人数
    std_num = len(User.objects.filter(teacher_id=teacher))
    essay_object = Essay.objects.filter(teacher_id = teacher)
    essayList = []
    for i in essay_object:
        temp = {}
        temp['title'] = i.title
        temp['due_time'] = i.due_time
        temp['essayid'] = i.id
        finish_num = 0
        set = User_Essay.objects.filter(essay_id = i )
        for j in set:
            if j.isSubmit == True :
                finish_num = finish_num + 1
        tempstr = str(finish_num)+"/"+str(std_num)
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

#查看学生的具体完成情况
#TODO:查看页面构思，最先做这个
def view(request):
    return HttpResponse('查看页面')

#学生管理
def std_manage(request):
    return

#个人信息管理，改密码之类的
def show_profile(request):
    return

def exit(request):
    del request.session['teacher_id']
    del request.session['name']
    return render(request, 'teacher/Login&Register.html')
