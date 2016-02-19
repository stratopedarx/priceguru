# -*- coding: utf-8 -*-
from core.currency.models import SupportedCurrency, CurrencyRatio
from django.contrib import admin

admin.site.register(SupportedCurrency)
admin.site.register(CurrencyRatio)