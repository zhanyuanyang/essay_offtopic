# coding:utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Teacher(models.Model):
    # 工号
    teacher_id = models.CharField(max_length=50, default='1')
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    avatar = models.CharField(max_length=30)

    def __unicode__(self):
        return self.teacher_id


class TrainedTopics(models.Model):
    trainedTopics = models.CharField(max_length=30)

    def __unicode__(self):
        return self.trainedTopics
