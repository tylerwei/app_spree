#from django.conf.urls import patterns, include, url
from mysite import settings
from mysite import dynamic_media_serve
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views.static import serve
from django.views.generic.simple import redirect_to
from django.conf.urls.static import static
from mysite.mmanapp.views import *
admin.autodiscover()
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

# for static files
site_media_url = settings.SITE_MEDIA_URL
if site_media_url.startswith('/'): site_media_url = site_media_url[1:]
media_url = settings.MEDIA_URL
if media_url.startswith('/'): media_url = media_url[1:]

print settings.STATIC_ROOT

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    (r'^admin/', include(admin.site.urls)),
    (r'^%s(?P<path>.*)$' % site_media_url, serve, {'document_root': settings.SITE_MEDIA_ROOT}),
    (r'^%s(?P<path>.*)$' % media_url, dynamic_media_serve.serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^login$', first_login),
    url(r'^pic/(?P<pid>\w+)/info$', get_pic_info),
    url(r'^pic/(?P<pid>\w+)/download$', check_login(download_pic)),
    url(r'^pic/(?P<pid>\w+)/comment/write$', check_login(write_comment)),
    url(r'^pic/(?P<pid>\w+)/comment/get/(?P<page>\d+)$', get_comment),
    url(r'^avatar/(?P<userid>\w+)$', get_avatar),
    url(r'^upload$', check_login(upload_pic)),
    url(r'^upload/test$', check_login(upload_pic_test)),
    url(r'^index/(?P<page>\d+)$', index),
    url(r'^me/(?P<page>\d+)$', check_login(get_me_info)),
    url(r'^pic/(?P<pid>\d+)/like$', check_login(set_liked_pic)),
    url(r'^user/(?P<userid>\w+)/info/(?P<page>\d+)$', get_user_info),
    #url(r'^.*$', error_404),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
