# -*- coding: utf-8 -*-
from .views import AddUrl, CheckTask, Main

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', Main.as_view(), name="main"),
                       url(r'add_url$', AddUrl.as_view(), name="add_url"),
                       url(r'is_ready/(?P<task_id>[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12})$', CheckTask.as_view(), name='check_task')
                       )
