#!/usr/bin/python
#-*- coding: UTF-8 -*-

import urllib, datetime, logging, sys
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.db.models import Q
from django.shortcuts import render_to_response

from mysite import settings
from mmanapp.lib import mmandef, mmanlogic
from mmanapp.api import oa_userinfo, oa_login
from mmanapp.models import *
from mmanapp.forms import *
from mmanapp.utils import log_exception

# Base Pages
# ==============================================
def global_init(request):
    # 全局变量初始化
    from mmanapp.lib import mmandef
    mmandef.g_username = ""
    mmandef.g_user = None
    mmandef.g_http_host = request.get_host()
    mmandef.g_request = request
    from django.forms import Form
    from mmanapp.forms import AddObjForm
    # 删除所有的clean_xxx字段校验方法
    kills = []
    klass = AddObjForm
    for attr in dir(klass):
        if attr.startswith("clean_"):
            kills.append(attr)
            delattr(klass, attr)
    attr = 'clean'
    if hasattr(klass, attr):
        if klass.clean != Form.clean:
            kills.append(attr)
            delattr(klass, attr)
    logging.debug("kill attrs: %s" % kills )
    return None

def Index(request):
    username = mmandef.g_username
    condition = Q(author=username)|Q(dev_users__contains=username)|Q(pdm_users__contains=username)|Q(syn_users__contains=username)
    closed = Q(state=MManSeq.State.finish)|Q(state=MManSeq.State.v2)
    seq_ing = MManSeq.objects.filter(condition).exclude(closed).order_by("-id")
    for seq in seq_ing:
        idc_finish = False
        if seq.state == seq.State.idcing:
            num = len(seq.get_mmanconf_set().exclude(outstat=mmandef.FlashOutstat.CONF_IDC))
            num += len(seq.get_mmanprogram_set().exclude(outstat=mmandef.FlashOutstat.IDC))
            num += len(seq.get_mmanmedia_set().exclude(outstat=mmandef.FlashOutstat.IDC))
            if num == 0:
                idc_finish = True
        seq.idc_finish = idc_finish
        seq.app = get_app(seq.appid_id)
    return render_to_response("index.html", {
        'hide_gohome': True,
        "seq_ing": seq_ing,
        })

def Succ(request,succtype,seqid):
    t_mdid = request.GET.get('mdid', None)
    return render_to_response('success.html', {
        'succtype':succtype,
        'seqid':seqid,
        'mdid':t_mdid,
        })

def onlyoa_login(view):
    def oa_login_func(request,*args,**kwargs):
        global_init(request)
        username = mmanlogic.get_username(request)
        if username is None:
            logging.error("not login. redirect to OA...")
            current_site = request.get_host()
            url = urllib.urlencode({'url':'http://'+current_site+request.path})
            param = urllib.urlencode({'url':'http://'+current_site+'/v3/loginsucc?%s'%url})
            return HttpResponseRedirect('http://passport.oa.com/modules/passport/signin.ashx?%s'%param)
        return view(request,*args,**kwargs)
    return oa_login_func
#装饰器用法
def login(view):
    def login_func(request, *args, **kwargs):
        global_init(request)
        username = mmanlogic.get_username(request)
        if username is None:
            logging.error("not login. redirect to OA...")
            current_site = request.get_host()
            url = urllib.urlencode({'url':'http://'+current_site+request.path})
            param = urllib.urlencode({'url':'http://'+current_site+'/v3/loginsucc?%s'%url})
            return HttpResponseRedirect('http://passport.oa.com/modules/passport/signin.ashx?%s'%param)

        user = mmanlogic.login_user(username)
        logging.debug("got user [%s], checking auth ... " % username)
        if username == "":
            msg = u'''抱歉，登录失败，无法检测您的用户名。<br/>
    （如果您是使用Outlook账号登录，请向 8000 申请访问 *.isd.com 的权限。）'''
            return render_to_response("intro.html", {"msg": msg})

        if 'test' not in sys.argv and user is None:
            msg = u'''%s'''%username
            return render_to_response("noright.html", {"user": msg})
        #暂时在日志中记录函数调用的总次数
        logging.getLogger('stat').error(u"total %s" % view.__name__)
        try:
            logging.debug("starting view %s()" % view.__name__)
            return view(request, *args, **kwargs)
        except Exception as e:
            #暂时在日志中记录函数调用失败的次数
            logging.getLogger('stat').error(u"failed %s" % view.__name__)
            log_exception(e)
            raise
    return login_func

def no_login(view):
    def new_view(request, *args, **kwargs):
        global_init(request)
        username = mmanlogic.get_username(request)
        user = mmanlogic.login_user(username)
        #暂时在日志中记录函数调用的总次数
        logging.getLogger('stat').error(u"total %s" % view.__name__)
        try:
            logging.debug("starting view %s()" % view.__name__)
            return view(request, *args, **kwargs)
        except Exception as e:
            #暂时在日志中记录函数调用失败的次数
            logging.getLogger('stat').error(u"failed %s" % view.__name__)
            log_exception(e)
            raise
    return new_view

def LoginSucc(request):
    url = request.GET.get('url', "/")
    response = HttpResponseRedirect(url)
    if 'ticket' in request.GET:
        ticket = request.GET['ticket']
        logging.debug("url_ticket:"+ticket)
        response.set_cookie('ticket',ticket)

        username, userid = oa_login.oa_decrypt_ticket(ticket)
        if username is None or userid is None:
            return HttpResponse("<CENTER style='font-size: 24px;'>登录失败。请联系管理员！</CENTER>")
        response.set_cookie('mm_fullname', username)
        response.set_cookie('mm_userid', userid)
        # CC页面需要mm_userid作为登录凭证
        if 'isd.com' in request.get_host():
            response.set_cookie('mm_fullname', username, domain="isd.com", max_age = 3600*24)
            response.set_cookie('mm_userid', userid, domain="isd.com", max_age = 3600*24)
            response.set_cookie('ticket',ticket, domain="isd.com", max_age = 3600*24)
        logging.error('user login: %s' % username)
    return response

def PartnerLogin(request):
    from mmanapp.forms import PartnerLoginForm
    if request.method == 'POST':
        form = PartnerLoginForm(request.POST)
        if not form.is_valid():
            return render_to_response("partner_login.html",
                    {'form': form})
        username = form.cleaned_data['username']
        try:
            userinfo = oa_userinfo.oa_userinfo(username)
        except Exception, e:
            log_exception(e)
            userinfo = {}

        if 'Id' not in userinfo:
            msg = u'''抱歉，无法获取您（%s）的RTX信息。''' % username
            return render_to_response("intro.html", {"msg": msg})
        userid = userinfo['Id']
        current_site = request.get_host()
        response = HttpResponseRedirect('http://%s/v3/' % current_site )

        response.set_cookie('ticket', username, max_age = 3600*24)
        response.set_cookie('mm_fullname', username, max_age = 3600*24)
        response.set_cookie('mm_userid', userid, max_age = 3600*24)
        if 'isd.com' in request.get_host():
            response.set_cookie('mm_userid', userid, domain="isd.com", max_age = 3600*24)
        logging.error('user login: %s' % username)
        return response
    else:
        form = PartnerLoginForm()
        return render_to_response("partner_login.html",
                {'form': form})


def Superman(request):
    supermans = [ u[0] for u in settings.ADMINS ]
    if mmandef.g_username not in supermans:
        return HttpResponse(u'你不是超人.')
    return render_to_response("superman.html")

def Hosts_add(request, appid):
    host_info = {}
    mman_app = get_object_or_404(MManAppid, appid=appid)#get_object_or_404
    supermans = [ u[0] for u in settings.ADMINS ]
    if mmandef.g_username not in supermans:
        return HttpResponse(u'你不是超人.')

    if request.method == 'POST':
        tmplist = []
        host_conf = request.POST.get("iplist", "")
        if host_conf == "":
            return render_to_response("hosts_add.html", {
                'host_conf':host_conf,
                })
        list_conf = host_conf.replace("\r\n", "\n").split("\n\n")
        for list_item in list_conf:
            if list_item == '':
                continue
            tmp_dict = {}
            list_conf_item = list_item.replace("\n\n","\n").split('\n')
            tmp_dict['iplist'] = list_conf_item[1:]
            if ":" not in list_conf_item[0]:
                msg = "标题格式不对，正确格式是\n===%d:xxx===" % i
                return render_to_response("hosts_add.html",
                        {'msg': msg, 'host_conf': host_conf})

            list_item = list_conf_item[0].replace("=", "").split(":")
            tmp_dict['type'] = list_item[0]
            tmp_dict['name'] = list_item[1]
            tmplist.append(tmp_dict)
        host_info['hosts'] = tmplist
        host_info['orgin'] = host_conf
        mman_app.host_info = repr(host_info)
        mman_app.save()
        return render_to_response("hosts_add.html",
                {'host_conf':host_conf})
    else:
        if mman_app.host_info == "":
            return render_to_response("hosts_add.html",
                    {'host_conf':mman_app.host_info})
        host_info_dict = str2dict(mman_app.host_info)
        return render_to_response("hosts_add.html", {
            'host_conf': host_info_dict.get("orgin", "")
            })

def Cgis_add(request, appid):
    mman_app = get_object_or_404(MManAppid, appid=appid)#get_object_or_404

    if request.method == 'POST':
        tmplist = []
        cgi_data = request.POST.get("cgi_lists", "")
        if cgi_data == "":
            return render_to_response("cgis_add.html", {
                'cgi_infos':cgi_data,
                })
        cgi_lists = cgi_data.replace("\r\n", "\n").split("\n")
        cgi_lists = [cgi for cgi in cgi_lists if len(cgi) > 0]
        prefer = str2dict(mman_app.prefer)
        prefer['cgi_lists'] = cgi_lists
        mman_app.prefer = repr(prefer)
        mman_app.save()
        return render_to_response('success.html', {
            'succtype':'index','msg':'配置检测接口设置成功！',
            })
    else:
        prefer = str2dict(mman_app.prefer)
        cgi_infos = ""
        if "cgi_lists" in prefer:
            cgi_infos = '\r\n'.join(prefer['cgi_lists'])
        return render_to_response("cgis_add.html", {
            'cgi_infos': cgi_infos, "mman_app":mman_app,
            })

def GotoCC(request, ccid):
    url = mmandef.g_ccurl_goto_cc % ccid
    username = mmandef.g_username
    userid = request.COOKIES.get("mm_userid", username)
    rsp = HttpResponseRedirect(url)
    rsp.set_cookie('ticket', username, domain='isd.com')
    rsp.set_cookie('mm_fullname', username, domain='isd.com')
    rsp.set_cookie('mm_userid', userid, domain='isd.com')
    return rsp

