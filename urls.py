# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.defaults import *
from django.contrib import admin
from django.views import static
from django.views.generic.simple import direct_to_template
from main.views import *

admin.autodiscover()

urlpatterns = patterns('',
    # the admin site
    (r'^admin/', include(admin.site.urls)),
    
    # main
    url(r'^survey/(?P<survey_id>.*)/$', survey, name='survey'),
    url(r'^thankyou/$', direct_to_template, {'template': 'main/thankyou.html'}, name='thank_you'),
    url(r'^expired/$', direct_to_template, {'template': 'main/expired.html'}, name='expired'),
    
    # json api
    url(r'^generate_link/(?P<customer_id>\d+)/(?P<formtype_id>\d+)/(?P<creation_date>\d{8})/$', generate_link, name='generate_link'),
    url(r'^generate_link/(?P<customer_id>\d+)/(?P<formtype_id>\d+)/$', generate_link, name='generate_link'),
    
    url(r'^survey_structure/$', survey_structure, name='survey_structure'),
    url(r'^survey_submit/(?P<form_id>\d+)/$', survey_submit, name='survey_submit'),
    url(r'^survey_range/(?P<from_date>\d{8})/(?P<to_date>\d{8})/(?P<submitted>[0-1])/$', survey_range, name='survey_range'),
    url(r'^survey_range/(?P<from_date>\d{8})/(?P<to_date>\d{8})/$', survey_range, {'submitted': 1}, name='survey_range'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', static.serve, {'document_root': settings.MEDIA_ROOT}),
    )
