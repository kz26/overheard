from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import *
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'site_main.views.index_view'),
    url(r'^select-school/$', 'site_main.views.select_school'),
    url(r'^login/$', 'site_main.views.site_login'),
    url(r'^logout/$', 'site_main.views.site_logout'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^post/(?P<postid>[0-9]+)/comment/$', 'site_main.views.post_comment'),
    url(r'^post/(?P<postid>[0-9]+)/like/$', 'site_main.views.like_post'),
    url(r'^(?P<school>[\w+-]+)/more_posts/$', 'site_main.views.more_posts'),
    url(r'^(?P<school>[\w+-]+)/more_posts/popular/$', 'site_main.views.more_posts_popular'),
    url(r'^(?P<school>[\w+-]+)/$', 'site_main.views.render_posts'),
    url(r'^fb_post_callback/(?P<postid>[0-9]+)/$', 'site_main.views.fb_post_callback'),
    url(r'^(?P<school>[\w+-]+)/user/(?P<userid>[0-9]+)/$', 'site_main.views.render_user_posts'),
    url(r'^(?P<school>[\w+-]+)/(?P<postid>[0-9]+)/$', 'site_main.views.render_single_post'),
    url(r'^(?P<school>[\w+-]+)/popular/$', 'site_main.views.render_posts_popular'),
    # Examples:
    # url(r'^$', 'overheard.views.home', name='home'),
    # url(r'^overheard/', include('overheard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
