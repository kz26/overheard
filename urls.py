from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import *
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^login/$', 'site_main.views.site_login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^post/(?P<postid>[0-9]+)/comment/$', 'site_main.views.post_comment'),
    url(r'^([\w+-]+)/$', 'site_main.views.render_posts'),
    # Examples:
    # url(r'^$', 'overheard.views.home', name='home'),
    # url(r'^overheard/', include('overheard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
