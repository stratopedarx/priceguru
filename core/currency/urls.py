# coding: utf-8
from core.currency.views import SetCurrencyView
from django.conf.urls import patterns, include, url
from django.views.generic.base import RedirectView

urlpatterns = patterns('',
                       url(r'^select/', SetCurrencyView.as_view(permanent=False), name='select'), #permanent=False because was warning
                       )
