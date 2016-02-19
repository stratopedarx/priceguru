# -*- coding: utf-8 -*-
from django.db.models import F, Func, Value, FloatField, CharField
from django.template import Library

register = Library()

@register.inclusion_tag('userprofile/item_info.html', takes_context=True)
def show_item_info(context, user_item):
    ccy = context['request'].COOKIES.get('currency')
    item_price = user_item.item.itemprice_set.order_by('-created_date').annotate(
        current_price_converted=F('current_price') * Func('currency', Value(ccy), function='get_currency_ratio', output_field=FloatField()),
        in_currency=Value(ccy, output_field=CharField())
    ).first()

    return {'price': item_price}
