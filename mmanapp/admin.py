#!/usr/bin/python
#-*- coding: UTF-8 -*-

from django.contrib import admin
from mysite.mmanapp.models import *
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin.widgets import FilteredSelectMultiple

class MManUserAdmin(admin.ModelAdmin):
    list_display = ('nick', 'userid', 'reg_time')
    list_filter = ('userid',)

class MManPicAdmin(admin.ModelAdmin):
    list_display = ('pic_id','user','title',)
    list_filter = ('pic_id',)
class MManCommentAdmin(admin.ModelAdmin):
    list_display = ('userid','pic','time',)
    list_filter = ('userid',)

admin.site.register(MManUser,MManUserAdmin)
admin.site.register(MManPic,MManPicAdmin)
admin.site.register(MManComment,MManCommentAdmin)
