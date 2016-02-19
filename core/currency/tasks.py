# -*- coding: utf-8 -*-
from datetime import timedelta
from celery.task import periodic_task
import itertools
from core.currency.models import SupportedCurrency, CurrencyRatio
import grab


@periodic_task(run_every=timedelta(hours=2))
def updale_currency_ratio():
    ccy_list = SupportedCurrency.objects.values_list("code", flat=True)

    g = grab.Grab()

    for from_ccy, to_ccy in itertools.product(ccy_list, repeat=2):
        g.go("http://www.xe.com/currencyconverter/convert/?Amount=1&From={0}&To={1}".format(from_ccy, to_ccy))
        ratio = float(g.doc.select("//td[@class='rightCol']/text()").text())

        obj, created = CurrencyRatio.objects.get_or_create(from_currency=from_ccy, to_currency=to_ccy)
        obj.ratio = ratio
        obj.save()
        print obj
