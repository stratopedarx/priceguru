# coding: utf-8
from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^i18n/', include('django.conf.urls.i18n')),
                       url(r'^', include("apps.main.urls", namespace="main")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^api/', include('core.api.urls', namespace='api')),
                       url(r'^user/', include('core.user.urls', namespace='user')),
                       url(r'^ajax/user/', include('core.user.ajax_urls', namespace='ajax/user')),
                       url(r'^currency/', include('core.currency.urls', namespace='currency')),
                       url(r'^loginza/', include('loginza.urls')),
                       url(r'^social/auth/', include('social.apps.django_app.urls', namespace='social'))
                       )
