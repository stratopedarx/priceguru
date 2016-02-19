# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url


from core.user.views.userprofile import \
    (ItemGroupCreateViewAjax, ItemGroupUpdateViewAjax, UserItemDeleteViewAjax,
     UserItemEditViewAjax,
     )

from core.user.views.user import \
    (UserSettingsChange,
     )

urlpatterns = patterns(
    '',
     url(r'itemgroup/add/$', ItemGroupCreateViewAjax.as_view(), name='itemgroup_add'),
     url(r'itemgroup/update/$', ItemGroupUpdateViewAjax.as_view(), name='itemgroup_update'),
     url(r'useritem/delete/$', UserItemDeleteViewAjax.as_view(), name='useritem_delete'),
     url(r'useritem/edit/$', UserItemEditViewAjax.as_view(), name='useritem_edit'),
     url(r'^change/$', UserSettingsChange.as_view(), name='change_ajax'),

)