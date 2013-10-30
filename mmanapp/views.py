#!/usr/bin/python
#-*- coding: UTF-8 -*-

import datetime, Image
import urllib, urllib2
import ImageFile
from django.http import Http404,HttpResponseRedirect
from mysite.mmanapp.lib.logic import *
from mysite.mmanapp.lib import mmandef
from mysite.mmanapp.forms import *
from mysite.mmanapp.models import *
from django.views.decorators.cache import cache_page



def first_login(request):
    if request.method != 'POST':
        return JsonResponse({'ecode': -1000, 'msg': u'method is error'})
    try:
        login_info = request.POST.get("login_info")
    except:
        return JsonResponse({'ecode': -1010, 'msg':u'params is uninvaild'})
    login_info = simplejson.loads(login_info)
    print login_info
    try:
        if int(login_info["ret"]) != 0:
            return JsonResponse({'ecode': -1010, 'msg':u'params is uninvaild'})
        #调用QQ接口
        print "test=========="
        openid = login_info["openid"]
        post_params = {
                "access_token": login_info["access_token"],
                "openid": openid,
                "oauth_consumer_key":"222222"
                }
        url = mmandef.QQ_GET_USERINFO_URL
        data = urllib.urlencode(post_params)
        req = urllib2.Request(url)
        fd = urllib2.urlopen(req, data)
        data = fd.read()
        pydata = simplejson.loads(data)
        if pydata["ret"] != 0:
            return JsonResponse({'ecode':-2006, 'msg':u'login error'})
        now_time = datetime.datetime.now()
        #注册新用户
        user = MManUser.objects.filter(userid=openid)
        if len(user) == 0:
            user = MManUser()
            user.userid = openid
        else:
            user = user[0]
        user.nick = pydata["nickname"]
        skey = create_skey(openid, time.mktime(now_time.timetuple()))
        user.skey = skey
        print skey
        user.skey_ctime = now_time
        user.avatar = pydata["figureurl_2"]
        user.save()
        print user
        #返回前台
        rsp = {'ecode':0, 'msg':u'ok'}
        rsp_data = {}
        #nick:昵称 avatar:头像 gender:性别
        rsp_data["nick"] = pydata["nickname"]
        rsp_data["gender"] = pydata["gender"]
        rsp["data"] = rsp_data
        response = JsonResponse(rsp)
        response.set_cookie('skey', skey, domain='talebook.org')
        response.set_cookie('user', openid, domain='talebook.org')
        print "====test====="
        print rsp
        print response
        return response
    except:
        print "except"
        return JsonResponse({'ecode': -1010, 'msg':u'params is uninvaild'})


def check_login(view):
    def login_func(request, *args, **kwargs):
        mmandef.g_user = None
        openid,skey = get_cookie(request)
        if openid is None and skey is None:
            print "test one"
            return JsonResponse({'ecode':-2005, 'msg':'user is not exist'});
        try:
            user = MManUser.objects.get(userid=openid)
        except:
            return JsonResponse({'ecode':-2005, 'msg':'user is not exist'});
        now_date = datetime.datetime.now()
        now_time = time.mktime(now_date.timetuple())
        if login_fail(user, skey, now_time):
            return JsonResponse({'ecode':-2005, 'msg':'user is not exist'});
        now_time = time.mktime(datetime.datetime.now().timetuple())
        user.last_login = user.skey_ctime
        user.skey_ctime = now_date
        user.save()
        mmandef.g_user = user
        return view(request, *args, **kwargs)
    return login_func

def demo_data():
    test_str = u'''{"data":{"picsize":"","blogs":[{"zanc":0,"photo_id":4459053,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201307/06/20130706081438_WyHVX.thumb.24_24_c.jpeg","cont":"= = 一定很挤吧","id":1595535,"name":"十年换不来的等待"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":40996738,"buylnk":"","albnm":"。插画菌～","iht":266,"albid":1733789,"favc":121,"ruid":813183,"id":80498612,"repc":1,"isrc":"http://cdn.duitang.com/uploads/item/201208/16/20120816122940_4weUu.thumb.200_0.jpeg","msg":"&lt;夏目友人帐&gt; 娘口森森 你在瓶子里做什么"},{"zanc":0,"photo_id":8208111,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":79703356,"buylnk":"","albnm":"。插画菌～","iht":296,"albid":1733789,"favc":101,"ruid":1119282,"id":80498502,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201306/05/20130605192557_YBkRw.thumb.200_0.jpeg","msg":"进击的巨人"},{"zanc":0,"photo_id":7945922,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":77034678,"buylnk":"","albnm":"。插画菌～","iht":352,"albid":1733789,"favc":26,"ruid":867924,"id":80498472,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201305/17/20130517204254_MMsJG.thumb.200_0.png","msg":"✿┞liran┦✿收图"},{"zanc":0,"photo_id":6728145,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":65263204,"buylnk":"","albnm":"。插画菌～","iht":280,"albid":1733789,"favc":4,"ruid":540993,"id":80498459,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201302/23/20130223173001_suBfk.thumb.200_0.jpeg","msg":"*瓶子里的小小世界*来自插画师Yasmine的插画作品，关于奇怪的瓶子们。Yasmine把每天生活的世界以及所想所感都绘制在可爱的“瓶子”里，这是她所喜爱的世界，也是她的灵感守护瓶。 手绘也不错"},{"zanc":0,"photo_id":5509732,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201209/03/20120903162201_32QSC.thumb.24_24_c.jpeg","cont":"都是你自己手绘的吗？","id":937530,"name":"打知嗒嗒"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":52044328,"buylnk":"","albnm":"。插画菌～","iht":282,"albid":1733789,"favc":70,"ruid":209821,"id":80498448,"repc":1,"isrc":"http://img4.duitang.com/uploads/item/201211/05/20121105200117_cyLTz.thumb.200_0.jpeg","msg":"╯з ︶ღ 麽麽"},{"zanc":0,"photo_id":2476131,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201205/13/20120513151837_NYS5d.thumb.24_24_c.jpeg","cont":"啊，以前看到过葬仪屋的瓶瓶，找到原形了","id":619692,"name":"七星瓢虫是益虫-嘎嘎"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":25359397,"buylnk":"","albnm":"。插画菌～","iht":1071,"albid":1733789,"favc":312,"ruid":448322,"id":80498414,"repc":1,"isrc":"http://cdn.duitang.com/uploads/item/201204/20/20120420103647_TFGYa.thumb.200_0.jpeg","msg":"瓶子里的动漫世界"},{"zanc":0,"photo_id":3732860,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":34769969,"buylnk":"","albnm":"。插画菌～","iht":240,"albid":1733789,"favc":32,"ruid":222692,"id":80498384,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201207/06/20120706173907_ikzCe.thumb.200_0.jpeg","msg":"在瓶子里的夏目~~好可爱！"},{"zanc":0,"photo_id":1950943,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201203/24/20120324100416_AyK3c.thumb.24_24_c.jpeg","cont":"感觉画中姑娘嘴唇干裂啊","id":468303,"name":"音乐之e"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":21727759,"buylnk":"","albnm":"。插画菌～","iht":283,"albid":1733789,"favc":130,"ruid":343198,"id":80498364,"repc":1,"isrc":"http://img4.duitang.com/uploads/item/201203/16/20120316131757_PQ2K8.thumb.200_0.jpeg","msg":"喜欢这种风格。。"},{"zanc":0,"photo_id":1381709,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":17333798,"buylnk":"","albnm":"。插画菌～","iht":266,"albid":1733789,"favc":161,"ruid":256490,"id":80498353,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201201/30/20120130204235_SmirQ.thumb.200_0.jpg","msg":"123 木头人"},{"zanc":0,"photo_id":2544697,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":25853030,"buylnk":"","albnm":"。插画菌～","iht":185,"albid":1733789,"favc":29,"ruid":448322,"id":70099699,"repc":0,"isrc":"http://cdn.duitang.com/uploads/item/201204/24/20120424150926_Ve4Xw.thumb.200_0.jpeg","msg":"【控首饰】混搭，森女，文艺范，清新学院派，复古，街头，轻摇滚.....各种风格混搭手绘插画，实用的穿衣教材 。"},{"zanc":0,"photo_id":4575972,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://cdn.duitang.com/uploads/people/201306/20/20130620110220_VdwC8.thumb.24_24_c.jpeg","cont":"面码~~","id":1543063,"name":"花的云端"},{"ava":"http://img4.duitang.com/uploads/people/201207/11/20120711214123_WnA2f.thumb.24_24_c.jpeg","cont":"面麻也~~~","id":806891,"name":"Duan璐维"},{"ava":"http://cdn.duitang.com/uploads/people/201302/07/20130207201325_JBdtP.thumb.24_24_c.jpeg","cont":"小面码","id":797421,"name":"童谣倾城"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":42133896,"buylnk":"","albnm":"。插画菌～","iht":324,"albid":1733789,"favc":165,"ruid":3054,"id":70088008,"repc":4,"isrc":"http://img4.duitang.com/uploads/item/201208/22/20120822215141_2mPGN.thumb.200_0.jpeg","msg":"萌妹纸"},{"zanc":0,"photo_id":5912203,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":56519121,"buylnk":"","albnm":"。插画菌～","iht":2365,"albid":1733789,"favc":12,"ruid":765461,"id":70087973,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201212/13/20121213143309_JSXxW.thumb.200_0.jpeg","msg":"好漂亮的手绘稿！惊艳！"},{"zanc":0,"photo_id":5668665,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":53850189,"buylnk":"","albnm":"。插画菌～","iht":791,"albid":1733789,"favc":10,"ruid":765461,"id":70087957,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201211/19/20121119231133_EQj3i.thumb.200_0.jpeg","msg":"植物创意插画"},{"zanc":0,"photo_id":6778909,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":65886608,"buylnk":"","albnm":"。插画菌～","iht":332,"albid":1733789,"favc":728,"ruid":568640,"id":70087901,"repc":0,"isrc":"http://cdn.duitang.com/uploads/item/201302/28/20130228202601_8EmkC.thumb.200_0.jpeg","msg":"【背景】埃菲尔铁塔"},{"zanc":0,"photo_id":3572315,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":33404567,"buylnk":"","albnm":"。插画菌～","iht":265,"albid":1733789,"favc":9,"ruid":341108,"id":70087860,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201206/26/20120626143111_Tuwjr.thumb.200_0.jpeg","msg":"SILVERRIDGESTUDIO"},{"zanc":0,"photo_id":2667279,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201309/03/20130903090709_JEryv.thumb.24_24_c.jpeg","cont":"我感觉也是那个","id":1758039,"name":"twilight暮"},{"ava":"http://cdn.duitang.com/uploads/people/201308/01/20130801151549_XvAmJ.thumb.24_24_c.jpeg","cont":"我猜应该是夏目友人账里的吧〜","id":1665301,"name":"姬之梦"},{"ava":"http://img4.duitang.com/uploads/people/201308/02/20130802182821_82QcG.thumb.24_24_c.jpeg","cont":"什么逻辑？","id":1671369,"name":"daphen939"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":26611193,"buylnk":"","albnm":"。插画菌～","iht":322,"albid":1733789,"favc":966,"ruid":97196,"id":70087837,"repc":6,"isrc":"http://img4.duitang.com/uploads/item/201205/01/20120501172309_QQdY5.thumb.200_0.jpeg","msg":"色调美"},{"zanc":0,"photo_id":7051338,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201304/18/20130418025148_fFdue.thumb.24_24_c.jpeg","cont":"我也抄了份","id":1424849,"name":"SZ代购"},{"ava":"http://img4.duitang.com/uploads/people/201304/14/20130414191004_uYKtn.thumb.24_24_c.jpeg","cont":"好萌~抱走啦","id":1418356,"name":"若纸"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":69130529,"buylnk":"","albnm":"。插画菌～","iht":323,"albid":1733789,"favc":707,"ruid":770897,"id":70087407,"repc":2,"isrc":"http://img4.duitang.com/uploads/item/201303/24/20130324161510_sFJzh.thumb.200_0.jpeg","msg":"你好，夏天【JO】"},{"zanc":0,"photo_id":6951488,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201302/10/20130210210452_a4E3n.thumb.24_24_c.jpeg","cont":"就是啊，太可爱啦~","id":1250578,"name":"天堂至简"},{"ava":"http://cdn.duitang.com/img/0/dfhead.thumb.24_24_c.gif","cont":"日系赫敏也太萌了♪(´ε｀ )","id":1414302,"name":"DOLLARS虞"},{"ava":"http://img4.duitang.com/uploads/people/201307/15/20130715180458_ET4aX.thumb.24_24_c.jpeg","cont":"貌似来自橘子酱男孩","id":1563226,"name":"大野猫YQL"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":68109016,"buylnk":"","albnm":"。插画菌～","iht":282,"albid":1733789,"favc":1196,"ruid":867924,"id":70087393,"repc":13,"isrc":"http://img4.duitang.com/uploads/item/201303/17/20130317154126_nKT3E.thumb.200_0.jpeg","msg":"✿┞liran┦✿收图7215967041"},{"zanc":0,"photo_id":5638331,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":53486782,"buylnk":"","albnm":"。插画菌～","iht":256,"albid":1733789,"favc":73,"ruid":841644,"id":63983188,"repc":0,"isrc":"http://cdn.duitang.com/uploads/item/201211/17/20121117083033_aukUm.thumb.200_0.jpeg","msg":"画风好好"},{"zanc":0,"photo_id":3536450,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":33119557,"buylnk":"","albnm":"。插画菌～","iht":337,"albid":1733789,"favc":180,"ruid":423109,"id":63983171,"repc":0,"isrc":"http://cdn.duitang.com/uploads/item/201206/24/20120624094220_wPCRZ.thumb.200_0.jpeg","msg":"夏达 的 将爱"},{"zanc":0,"photo_id":3200510,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":30453606,"buylnk":"","albnm":"。插画菌～","iht":300,"albid":1733789,"favc":187,"ruid":172120,"id":63976061,"repc":0,"isrc":"http://img4.duitang.com/uploads/item/201206/03/20120603132052_jQhSj.thumb.200_0.jpeg","msg":"很多时候，努力并不是为了得到奖赏，而是为了被认同。"},{"zanc":0,"photo_id":5908108,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/uploads/people/201305/06/20130506192602_YjrMn.thumb.24_24_c.jpeg","cont":"不知道诶","id":1465900,"name":"LES--LEY"},{"ava":"http://img4.duitang.com/uploads/people/201111/12/20111112142132_PBNFn.thumb.24_24_c.jpg","cont":"请问这个的作者是？","id":158723,"name":"Tlp王子奕"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":56466761,"buylnk":"","albnm":"。插画菌～","iht":230,"albid":1733789,"favc":560,"ruid":261016,"id":63975855,"repc":2,"isrc":"http://img4.duitang.com/uploads/item/201212/12/20121212222610_Cmhyk.thumb.200_0.jpeg","msg":"只有我被自己的爱溺死"},{"zanc":0,"photo_id":4612394,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":42445636,"buylnk":"","albnm":"。插画菌～","iht":266,"albid":1733789,"favc":293,"ruid":741731,"id":63975829,"repc":0,"isrc":"http://cdn.duitang.com/uploads/item/201208/24/20120824202858_8wTHs.thumb.200_0.jpeg","msg":"清瘦单薄的美骚年"},{"zanc":0,"photo_id":5395672,"unm":"雁亦亦亦亦","uid":1053025,"cmts":[{"ava":"http://img4.duitang.com/img/0/dfhead.thumb.24_24_c.gif","cont":"帅","id":1304750,"name":"酸ai"},{"ava":"http://cdn.duitang.com/uploads/people/201212/10/20121210134448_UkY58.thumb.24_24_c.jpeg","cont":"看见制服走不动星人路过。。。。。。。。","id":778085,"name":"加菲0403"},{"ava":"http://cdn.duitang.com/uploads/people/201211/21/20121121195504_KhhQk.thumb.24_24_c.jpeg","cont":"帅锅~","id":115931,"name":"日子很薄but梦想很厚"}],"sta":0,"good":false,"common":false,"ava":"http://img4.duitang.com/uploads/people/201211/02/20121102205120_UYWeX.thumb.24_24_c.jpeg","coupon_price":0,"price":0,"rid":50776199,"buylnk":"","albnm":"。插画菌～","iht":287,"albid":1733789,"favc":416,"ruid":671681,"id":63975147,"repc":3,"isrc":"http://img4.duitang.com/uploads/item/201210/27/20121027094251_n24jA.thumb.200_0.jpeg","msg":"别告诉我你不是制服控"}],"hasrp":true,"has_next":true,"pgsource":"ad_","coupon":false,"nopth":true},"success":true}
    '''
    python_object = simplejson.loads(test_str)
    json_dict = {}
    data_dict = {}
    data = python_object["data"]
    new_blogs = []
    blogs = data["blogs"]
    i = 5000
    for item in blogs:
        tmp_dict = {}
        tmp_dict["pid"] = str(i)
        tmp_dict["like"] = i
        tmp_dict["comment_num"] = i
        tmp_dict["price"] = 0
        tmp_dict["title"] = str(i)
        tmp_dict["desc"] = item["msg"]
        tmp_dict["width"] = 200
        tmp_dict["height"] = item["iht"]
        tmp_dict["url"] = item["isrc"]
        new_blogs.append(tmp_dict)
        data_dict[i] = tmp_dict
        i = i - 1
    return new_blogs


@cache_page(60 * 1)
def index(request, page):
    page = int(page)
    if page < 0:
        JsonResponse({'ecode': -1006, 'msg': u'page is uninvaild'})
    pre_page = page
    page = page + 1
    pics = MManPic.objects.all()[pre_page*mmandef.BASE_INDEX:page*mmandef.BASE_INDEX].values()
    pic_len = len(pics)
    if pic_len == 0:
        JsonResponse({'ecode': 0, 'msg': u'ok', 'data':{'pic_size':0, 'pics':''}})
    data = {}
    pic_list = []
    for pic in pics:
        item = {'width':200, 'height':200, 'price':0}
        item["pid"] = pic["pic_id"]
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
        item["url"] = mmandef.PIC_PRE_URL + pic["imagedata"] + '?width=200' #url_suffix
        pic_list.append(item)
    pic_list.extend( demo_data() )
    data["pics"] = pic_list
    data["pic_size"] = pic_len
    result = {}
    result["data"] = data
    result["ecode"] = 0
    result["msg"] = u"ok"
    return JsonResponse(result)


def upload_pic(request):
    user = mmandef.g_user
    print user
    if request.method != 'POST':
        print "abc"
        return JsonResponse({'ecode': -1000, 'msg': u'method is error'})
    try:
        #filedata = request.FILES["filename"].content
        filename = request.FILES["file"].name
        print filename
        f = request.FILES["file"]
        print f
    except:
        print "testst"
        return JsonResponse({'ecode': -1001, 'msg':'POST data error'})
    form = PicForm(request.POST)
    print form
    if form.is_valid():
        cd = form.cleaned_data
        try:
            pic = MManPic()
            pic.user = user
            pic.pic_id = get_pic_id(f.read())
            print pic.pic_id
            pic.imagedata.save(pic.pic_id+".jpg", f)
            print "test========1234"
            pic.filename = filename
            pic.desc = cd["desc"]
            pic.title = cd["title"]
            info_dict = {}
            info_dict["size"] = len(pic.imagedata)
            info_dict["height"] = cd["height"]
            info_dict["width"] = cd["width"]
            pic.info = str(info_dict)
            pic.save()
        except Exception as e:
            print e
        print pic.pic_id
        rsp = {'ecode':0, 'msg':u'ok'}
        data = {'pid': pic.pic_id, 'url': mmandef.PIC_PRE_URL + pic.imagedata.name}
        rsp["data"] = data
        return JsonResponse(rsp)
    else:
        print "is not vaild"
        return JsonResponse({'ecode': -1001, 'msg':'POST data error'})

def upload_pic_test(request):
    user = mmandef.g_user
    print user
    if request.method != 'POST':
        print "abc"
        return JsonResponse({'ecode': -1000, 'msg': u'method is error'})
    try:
        #filedata = request.FILES["filename"].content
        filename = request.FILES["file"].name
        f = request.FILES["file"]
    except:
        return JsonResponse({'ecode': -1001, 'msg':'POST data error'})
    form = PicForm(request.POST)
    print form
    if form.is_valid():
        cd = form.cleaned_data
        try:
            pic = MManPic()
            pic.user = user
            pic.pic_id = get_pic_id(f.read())
            print pic.pic_id
            print f
            pic.imagedata.save(pic.pic_id, f)
            img = Image.open(f)
            width = int(img.size[0])
            height = int(img.size[1])
            s_width = 200
            #s_height = int((width/200.0) * height)
            s_height = 100
            m_width = 600
            m_height = 300
            #m_height = int((width/600.0) * height)
            img.thumbnail((s_width,s_height),Image.ANTIALIAS)
            pic.s_imagedata.save(pic.pic_id, img)
            img.thumbnail((m_width,m_height),Image.ANTIALIAS)
            pic.m_imagedata.save(pic.pic_id, img)
            pic.filename = filename
            pic.desc = cd["desc"]
            pic.title = cd["title"]
            info_dict = {}
            info_dict["size"] = len(pic.imagedata)
            info_dict["height"] = cd["height"]
            info_dict["width"] = cd["width"]
            info_dict["m_height"] = m_height
            info_dict["m_width"] = m_width
            info_dict["s_height"] = s_height
            info_dict["s_width"] = s_width
            pic.info = str(info_dict)
            pic.save()
        except Exception as e:
            print e
        print pic.pic_id
        rsp = {'ecode':0, 'msg':u'ok'}
        data = {'pid': pic.pic_id, 'url': mmandef.PIC_PRE_URL + pic.imagedata.name}
        rsp["data"] = data
        return JsonResponse(rsp)
    else:
        print "is not vaild"
        return JsonResponse({'ecode': -1001, 'msg':'POST data error'})

@cache_page(60 * 3)
def get_pic_info(request, pid):
    if request.method != 'GET':
        return JsonResponse({'ecode': -1000, 'msg': u'method is error'})
    try:
        pic = MManPic.objects.get(pic_id=pid)
    except:
        return JsonResponse({'ecode': -1004, 'msg': u'pic is not exist'})
    #path = "orgin/" + time + "/" + pid
    #if path != pic.imagedata.name:
        #return JsonResponse({'ecode': -1005, 'msg': u'url is uninvaild'})
    rsp = {'ecode':0, 'msg':u'ok'}
    data = {'width': 0, 'height':0}
    data["liked"] = pic.like_num
    data["commented"] = pic.comments_num
    data["downloaded"] = 1
    info = str2dict(pic.info)
    if "width" in info:
        data["width"] = info["width"]
    if "height" in info:
        data["height"] = info["height"]
    data["owner"] = pic.user.userid
    data["nick"] = pic.user.nick
    rsp["data"] = data
    return JsonResponse(rsp)

def set_liked_pic(request, pid):
    if mmandef.g_user is None:
        return JsonResponse({'ecode':-2005, 'msg':'user is not exist'});
    try:
        pic = MManPic.objects.get(pic_id=pid)
        pic.like_num = pic.like_num + 1
        pic.save()
    except:
        return JsonResponse({'ecode': -1004, 'msg': u'pic is not exist'})
    return JsonResponse({'ecode':0, 'msg': u'ok'})

def get_me_info(request, page):
    page = int(page)
    if page < 0:
        JsonResponse({'ecode': -1006, 'msg': u'page is uninvaild'})
    user = mmandef.g_user
    pre_page = page
    page = page + 1
    rsp = {'ecode':0, 'msg':u'ok'}
    print user
    pics = user.mmanpic_set.all()[pre_page*mmandef.BASE_INDEX:page*mmandef.BASE_INDEX].values()
    data = {}
    data["nick"] = user.nick
    data["intro"] = user.intro
    data["pic_num"] = user.upload_pics_num
    data['money'] = user.money
    data['pics'] = get_upload_pics(pics)
    rsp["data"] = data
    return JsonResponse(rsp)

def write_comment(request, pid):
    if request.method != 'POST':
        return JsonResponse({'ecode': -1000, 'msg': u'method is error'})
    content = request.POST.get("content", "")
    if content == "":
        return JsonResponse({'ecode': -1004, 'msg': u'params user is not exist'})
    try:
        pic = MManPic.objects.get( pic_id=pid )
        comment = MManComment()
        comment.pic = pic
        comment.userid = mmandef.g_user.userid
        comment.nick = mmandef.g_user.nick
        comment.content = content
        comment.save()
    except:
        return JsonResponse({'ecode': -1006, 'msg': u'系统繁忙，请稍候再试'})
    return JsonResponse({'ecode':0, 'msg': u'ok'})

def get_comment(request, pid, page):
    try:
        pic = MManPic.objects.get(pic_id=pid)
    except:
        JsonResponse({'ecode': -1005, 'msg': u'该图片不存在'})
    page = int(page)
    if page < 0:
        JsonResponse({'ecode': -1006, 'msg': u'page is uninvaild'})
    pre_page = page
    page = page+1
    comms  = pic.mmancomment_set.all().order_by('time')[pre_page*mmandef.BASE_INDEX:page*mmandef.BASE_INDEX].values()
    comment_len = len(comms)
    if comment_len == 0:
        JsonResponse({'ecode': 0, 'msg': u'ok', 'data':{'comment_size':0, 'comments':''}})
    data = {}
    comment_list = []
    for comm in comms:
        item = {}
        item["nick"] = comm["nick"]
        item["userid"] = comm["userid"]
        item["time"] = comm["time"]
        item["content"] = comm["content"]
        comment_list.append(item)
    data["comments"] = comment_list
    data["comment_size"] = comment_len
    result = {"ecode":0, "msg": u"ok"}
    result["data"] = data
    return JsonResponse(result)

def download_pic(request, pid):
    try:
        pic = MManPic.objects.get(pic_id = pid)
    except:
        return JsonResponse({'ecode': -1005, 'msg': u'该图片不存在'})
    user = mmandef.g_user.money
    #if pic.user.userid == user.userid:
    if user.money < 1:
        return JsonResponse({'ecode': -1015, 'msg': u'您的金币不足，无法下载该图片'})
    user.money = user.money - 1
    user.save()
    pic.imagedata.open(mode='rb')
    data = pic.imagedata.read()
    pic.imagedata.close()
    filename = pic.filename()
    response = HttpResponse(data,mimetype='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response

def get_avatar(request, userid):
    try:
        user = MManUser.objects.get(userid=userid)
    except:
        raise Http404
    return HttpResponseRedirect(user.avatar)

def get_user_info(request, userid, page):
    try:
        user = MManUser.objects.get(userid=userid)
    except:
        return JsonResponse({'ecode': -1006, "msg":u'您所访问的用户不存在'})
    page = int(page)
    if page < 0:
        JsonResponse({'ecode': -1006, 'msg': u'page is uninvaild'})
    pre_page = page
    page = page + 1
    rsp = {'ecode':0, 'msg':u'ok'}
    pics = user.mmanpic_set.all()[pre_page*mmandef.BASE_INDEX:page*mmandef.BASE_INDEX].values()
    data = {}
    data["nick"] = user.nick
    data["intro"] = user.intro
    data["pic_num"] = user.upload_pics_num
    data['money'] = user.money
    data['pics'] = get_upload_pics(pics)
    rsp["data"] = data
    return JsonResponse(rsp)
