# -*- coding: utf-8 -*-
from datetime import timedelta
from core.api.models import UserItem, ItemPrice
from django.db.models import F, Func, Value, FloatField, CharField
from django.template import Library
from django.utils.timezone import now

register = Library()

@register.inclusion_tag('userprofile/charts.html', takes_context=True)
def show_chart(context, group):
    result = {}
    result[group.group_name] = {}
    for u_item in UserItem.objects.filter(group_id=group.id).values("item__id", "custom_name", 'item__source__partner__name'):
        result[group.group_name][(u_item['custom_name'], u_item['item__source__partner__name'])] = (ItemPrice.objects.filter(
            item_id=u_item['item__id'],
            created_date__gte=now()-timedelta(days=7)
        )
            .order_by("created_date")
            .annotate(current_price_converted=F("current_price")*Func(F("currency"),
                                                                      Value(context['request'].COOKIES.get("currency")),
                                                                      function='get_currency_ratio',
                                                                      output_field=FloatField()))
            .values_list("created_date", "current_price_converted"))

    return dict(data=result, group=group, currency=context['request'].COOKIES.get("currency"))
