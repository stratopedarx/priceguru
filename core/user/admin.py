# -*- coding: utf-8 -*-
from core.user.models import User
from django.contrib import admin
from .forms.user import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin


class UserAdmin(DjangoUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    suit_form_tabs = (('general', 'General'),
                      ('info', 'User info'),
                      ('advanced', 'Advanced settings'))

    fieldsets = [
        (None, {
            'classes': ('suit-tab suit-tab-general',),
            'fields': ['username', 'email', 'is_active']
        }),
        (None, {
            'classes': ('suit-tab suit-tab-info',),
            'fields': ['first_name', 'last_name']}),
        (None, {
            'classes': ('suit-tab suit-tab-advanced',),
            'fields': ['password',
                       'groups', 'user_permissions',
                       'date_joined', 'last_login']}),
    ]

    readonly_fields = ['date_joined', 'last_login']

admin.site.register(User, UserAdmin)