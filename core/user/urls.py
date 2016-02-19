# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url

from core.user.views.user import (
    LoginView, LogoutView,
    RegisterView, RegisterSuccessView,
    RestorePasswordRequestView, RestorePasswordRequestDoneView, UserPage, UserSettingsView,
)
from core.user.views.userprofile import (
    UserProfileView, UserProfileItemGroupView,
    ItemGroupCreateView, ItemGroupDeleteView,
    UserItemUpdateView, UserItemDeleteView,

)
from ..user.views.loginza_view import complete_registration


urlpatterns = patterns(
    '',
    url(r'^(?P<pk>\d+)/$', UserPage.as_view(), name='user'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^register/success/$', RegisterSuccessView.as_view(), name='register_success'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    # login using loginza
    url(r'^complete_registration/$', complete_registration, name='users_complete_registration'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^change/password/$', RestorePasswordRequestView.as_view(), name='change_password'),
    url(r'^change/password/done/$', RestorePasswordRequestDoneView.as_view(), name='change_password_done'),
    # user profile
    url(r'^$', UserProfileView.as_view(), name='userprofile'),
    url(r'^settings/$', UserSettingsView.as_view(), name='settings'),
    url(r'^itemgroup/$', UserProfileView.as_view(), name='itemgroups'),
    url(r'^itemgroup/(?P<pk>\d+)/$', UserProfileItemGroupView.as_view(), name='itemgroup'),
    url(r'^itemgroup/add/$', ItemGroupCreateView.as_view(), name='itemgroup_add'),
    url(r'^itemgroup/(?P<pk>\d+)/delete/$', ItemGroupDeleteView.as_view(), name='itemgroup_delete'),
    url(r'^itemgroup/item/(?P<pk>\d+)/edit/$', UserItemUpdateView.as_view(), name='useritem_edit'),
    url(r'^itemgroup/item/(?P<pk>\d+)/delete/$', UserItemDeleteView.as_view(), name='useritem_delete'),
)
