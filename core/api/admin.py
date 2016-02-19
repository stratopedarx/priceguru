# -*- coding: utf-8 -*-
from django.contrib import admin
from models import *



class PartnerSourceAdmin(admin.StackedInline):
    model = PartnerSource
    extra = 0

class UserItemAdmin(admin.StackedInline):
    model = UserItem
    extra = 0


class PartnerAdmin(admin.ModelAdmin):
    inlines = [PartnerSourceAdmin,]


class ItemGroupAdmin(admin.ModelAdmin):
    inlines = [UserItemAdmin,]

admin.site.register(Partner, PartnerAdmin)
admin.site.register(OriginalItem)
admin.site.register(UserItem)

admin.site.register(ItemPrice)
admin.site.register(ItemGroup, ItemGroupAdmin)
admin.site.register(PartnerSource)
