# -*- coding: utf-8 -*-

from django.db.models import Count, F

from core.api.models import ItemGroup


def user(request):
    item_groups = []
    if request.user.is_authenticated():
                item_groups = ItemGroup.objects.filter(user=request.user).annotate(itemscount=Count('useritem'))
                return {
                "user": request.user,
                "groups": item_groups,
                }

    else:
        return {
            "user": None,
        }
