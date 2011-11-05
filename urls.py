from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'index.html'}),
    url(r'^login/$', 'site_main.views.site_login'),
    url(r'^logintest/$', 'site_main.views.logintest'),
    # Examples:
    # url(r'^$', 'overheard.views.home', name='home'),
    # url(r'^overheard/', include('overheard.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
