#coding:utf-8
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import collections
import django.utils.timezone as timezone
# Create your models here.

class Essay(models.Model):
    #作文题目
    title = models.CharField(max_length=100,default='no title')
    #作文截止时间
    due_time = models.DateField(default="2017-01-01")
    #作文类型
    AUTONOMOUS = 'AT'
    PLAN = 'PL'
    ESSAY_TYPE_CHOICES = (
        (AUTONOMOUS, 'Autonomous'),
        (PLAN,'Plan'),
    )
    type = models.CharField(max_length=2,
                                      choices=ESSAY_TYPE_CHOICES,
                                      default=AUTONOMOUS)

    def is_upperclass(self):
        return self.type in (self.AUTONOMOUS, self.PLAN)

class User_Essay(models.Model):
    create_date = models.DateField('保存日期',default = timezone.now)
    update_date = models.DateField('最后修改日期',auto_now = True)
    user_title = models.CharField(max_length=100,default="")
    content = models.CharField(max_length=350,default="")
    isSubmit = models.BooleanField(default=False)
    #FK:user_id essay_id
    essay_id = models.ForeignKey('Essay')
    user_id = models.ForeignKey('User')
    def __unicode__(self):
        return self.create_date


class User(models.Model):
    user_id = models.CharField(max_length=50)
    actual_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.CharField(max_length=30)
    exp = models.IntegerField()

    def __unicode__(self):
        return self.name

class Report(models.Model):
    isOffTopic = models.BooleanField()
    score = models.CharField(max_length=5)
    # errorlist = JSONField()
    error = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    chart1 = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    chart2 = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    detail = JSONField(load_kwargs={'object_pairs_hook': collections.OrderedDict})
    feedback = models.CharField(max_length = 50,default="无")
    essay_id = models.ForeignKey('Essay')
    user_id = models.ForeignKey('User')
    def __unicode__(self):
        return self.user_id,self.essay_id
# # class ErrorField(models.Field):

#
# result ={}
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
