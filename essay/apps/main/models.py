# coding:utf-8
from __future__ import unicode_literals

from django.db import models
from jsonfield import JSONField
import collections
import django.utils.timezone as timezone




class Essay(models.Model):
    # 作文题目
    title = models.CharField(max_length=100, default='no title')
    # 作文截止时间
    due_time = models.DateField(default="2017-01-01")
    # 作文类型
    AUTONOMOUS = 'AT'
    PLAN = 'PL'
    description = models.CharField(max_length=200, default='no description')
    ESSAY_TYPE_CHOICES = (
        (AUTONOMOUS, 'Autonomous'),
        (PLAN, 'Plan'),
    )
    type = models.CharField(max_length=2,
                            choices=ESSAY_TYPE_CHOICES,
                            default=AUTONOMOUS)
    teacher_id = models.ForeignKey('teacher.Teacher')

    def is_upperclass(self):
        return self.type in (self.AUTONOMOUS, self.PLAN)


class User_Essay(models.Model):
    create_date = models.DateField('保存日期', default=timezone.now)
    update_date = models.DateField('最后修改日期', auto_now=True)
    user_title = models.CharField(max_length=100, default="")
    content = models.CharField(max_length=350, default="")
    isSubmit = models.BooleanField(default=False)
    # FK:user_id essay_id
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
    teacher_id = models.ForeignKey('teacher.Teacher')

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
    feedback = models.CharField(max_length=50, default="无")
    essay_id = models.ForeignKey('Essay')
    user_id = models.ForeignKey('User')

    def __unicode__(self):
        return self.user_id, self.essay_id
