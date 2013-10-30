#!/usr/bin/python
#-*- coding: UTF-8 -*-

from django import template

register = template.Library()

from django.template import Node
from django.template import Library
from django.conf import settings
from django.utils.html import escape

def load_args(context):
    context["URL_MEDIA"] = settings.SITE_MEDIA_URL
    context["URL_BASE"] = settings.SITE_BASE_URL
    return

@register.tag('load_basic')
def load_basic(parser, token):
    class UrlNode(Node):
        def render(self, context):
            return load_args(context)
    return UrlNode()

