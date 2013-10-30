#!/usr/bin/python
#-*- coding: UTF-8 -*-

import logging
import datetime
from django.db import models
#from django.db.models.fields.files import ImageFieldFile
from mysite.mmanapp.lib.logic import *
from django.http import HttpResponse

MODEL_APP_NAME = "mmanapp"

#user
class MManUser(models.Model):
    userid    = models.CharField(primary_key=True,max_length=128, db_index=True)
    skey     = models.CharField(max_length=128)
    avatar = models.CharField(max_length=512, blank=True, null=True)

    email    = models.EmailField(blank=True, null=True)

    upload_pics_num = models.IntegerField(default=0)
    reg_time = models.DateTimeField(auto_now_add=True, default=datetime.datetime.now)
    last_login = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
    skey_ctime = models.DateTimeField(default=datetime.datetime.now)
    money  = models.IntegerField(default=0)
    nick = models.CharField(max_length=256)
    intro = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        app_label = MODEL_APP_NAME
        pass
    def __unicode__(self):
        return unicode(self.nick)

class MManPic(models.Model):
    pic_id   = models.CharField(primary_key=True, max_length=512)
    user = models.ForeignKey(MManUser,blank=True,null=True)
    imagedata = models.ImageField(upload_to=get_upload_path("orgin/"))

    m_imagedata = models.ImageField(upload_to=get_upload_path("mid/"),blank=True,null=True)
    s_imagedata = models.ImageField(upload_to=get_upload_path("small/"),blank=True,null=True)

    title = models.CharField(max_length=128)
    desc  = models.CharField(max_length=512)
    filename = models.CharField(max_length=512)
    comments_num = models.IntegerField(default=0)
    like_num = models.IntegerField(default=0)
    info = models.TextField(blank=True,null=True)
    time = models.DateTimeField(auto_now=True, default=datetime.datetime.now)

    class Meta:
        app_label = MODEL_APP_NAME
        ordering = ['pic_id','like_num','comments_num']
        pass
    def __unicode__(self):
        return  unicode(self.pic_id)

    def get_info(self):
        return str2dict(self.info)

    def __getattr__(self, name):
        info = self.get_info()
        if name in info:
            return info[name]
        elif hasattr(self, "_default_info") and name in self._default_info:
            logging.info("[%d] getattr from default_info" %self.pic_id)
            return self._default_info[name]
        raise AttributeError(name)


class MManComment(models.Model):
    nick = models.CharField(max_length=256)
    avatar = models.CharField(max_length=512, blank=True, null=True)
    userid    = models.CharField(primary_key=True,max_length=128, db_index=True)
    #userid = models.ForeignKey(MManUser)
    pic = models.ForeignKey(MManPic)
    time = models.DateTimeField(auto_now=True, default=datetime.datetime.now)
    content = models.TextField(max_length=512)

    class Meta:
        app_label = MODEL_APP_NAME
        ordering = ['time']
        pass
    def __unicode__(self):
        return  unicode(self.content)

