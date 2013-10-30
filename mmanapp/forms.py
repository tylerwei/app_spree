#!/usr/bin/python
#-*- coding: UTF-8 -*-

import copy,logging

from django import forms
from django.forms import ModelForm
from django.utils import simplejson
from django.db.models import Q

class PicForm(forms.Form):
    desc = forms.CharField(max_length=512, required=False)
    title = forms.CharField(max_length=256, required=False)
    height = forms.IntegerField(required=True)
    width = forms.IntegerField(required=True)

    def clean_height(self):
        height = self.cleaned_data["height"]
        if height < 100:
            raise forms.ValidationError("Not enough height!")
        return height
    def clean_width(self):
        width = self.cleaned_data["width"]
        if width< 100:
            raise forms.ValidationError("Not enough width!")
        return width
