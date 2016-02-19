# -*- coding: utf-8 -*-
from apps.main.views import IndexView
from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
)
