#!/usr/bin/python
#-*- coding: UTF-8 -*-

import hashlib,random,time
import logging, urllib, os, re, sys, datetime, string, types
from django.utils import simplejson
from django.http import HttpResponse
from mysite.mmanapp.models import *
from mysite.mmanapp.lib import mmandef

def create_skey(openid, now_time):
    rand = random.randint(1, 1000000000)
    key = str(rand) + str(now_time) + str(openid)
    return hashlib.md5(key).hexdigest()

def login_fail(user, skey, now_time):
    if now_time - time.mktime(user.skey_ctime.timetuple()) > 7776000:
        return True
    if user.skey != skey:
        return True
    return False

def get_cookie(request):
    cs = request.COOKIES
    if 'skey' in cs and 'user' in cs:
        return (cs["user"], cs["skey"])
    else:
        return (None, None)

def get_pic_id(filename):
    name = hashlib.md5(filename).hexdigest()
    #name = hash.update(filename).hexdigest()
    rand = str(random.randint(1, 100000000000))
    return hashlib.md5(rand + name).hexdigest()


def get_upload_path(path_prefix):
    ''' 根据指定的路径前缀，返回一个路径处理函数 '''
    def get_upload_path_(instance, filename):
        prefix = path_prefix
        date = datetime.datetime.now().strftime("%Y%m")
        #return "%(prefix)s/%(date)s/%(name)s" % vars()
        return "%s%s/%s" % (prefix, date, filename)
    return get_upload_path_

def py2json(pydata, indent=4):
    from datetime import date, datetime
    def default(obj):
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        else:
            raise TypeError, '%r is not JSON serializable' % obj

    return simplejson.dumps(pydata, ensure_ascii=False,
            default = default, sort_keys=True, indent=indent)

def JsonResponse(pydata):
    return HttpResponse( py2json(pydata) )

def error_log(request, msg):
    logging.error("%s %s" % (mmandef.g_username, msg))

def info_log(request, msg):
    logging.info("%s %s" % (mmandef.g_username, msg))



def str2list(str_val):
    if str_val is None:
        return []
    elif isinstance(str_val, list):
        return str_val
    elif isinstance(str_val, (str, unicode)) and len(str_val) < 2:
        return []
    else:
        return eval(str_val)

def str2dict(str_val):
    if str_val is None:
        return {}
    elif isinstance(str_val, dict):
        return str_val
    elif isinstance(str_val, (str, unicode)) and len(str_val) < 2:
        return {}
    else:
        return eval(str_val)

def atoi(val):
    try: return int(val)
    except: return 0

def get_upload_pics(pics):
    upload_pics = []
    for pic in pics:
        item = {'width':200, 'height':200, 'price':0}
        item["pid"] = pic["imagedata"]
        item["title"] = pic["title"]
        item["desc"] = pic["desc"]
        item["like"] = pic["like_num"]
        item["comment_num"] = pic["comments_num"]
        info = str2dict(pic["info"])
        if "width" in info:
            item["width"] = info["width"]
        if "height" in info:
            item["height"] = info["height"]
        url_suffix = mmandef.PIC_SUFFIX % (item['height'] / 4, item['width'] / 4)
        item["url"] = mmandef.PIC_PRE_URL + pic["imagedata"] + url_suffix
        upload_pics.append(item)
    return upload_pics


