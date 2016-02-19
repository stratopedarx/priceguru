# -*- coding: utf-8 -*-
from core.currency.models import SupportedCurrency
from django.template import Library

register = Library()


@register.inclusion_tag("currency/select.html", takes_context=True)
def select_currency(context):
    return dict(currency=context['request'].COOKIES.get("currency"),
                next=context['request'].build_absolute_uri(),
                currencies_list=SupportedCurrency.objects.values_list("code", flat=True))