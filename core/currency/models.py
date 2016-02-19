# -*- coding: utf-8 -*-
from django.db import models


class SupportedCurrency(models.Model):
    code = models.CharField(max_length=3)

    def __unicode__(self):
        return self.code


class CurrencyRatio(models.Model):
    from_currency = models.CharField(max_length=3)
    to_currency = models.CharField(max_length=3)
    ratio = models.FloatField(default=1.0)
    updated_at = models.DateField(auto_now=True)

    def __unicode__(self):
        return u"{self.from_currency}-{self.to_currency}: {self.ratio}".format(self=self)

    class Meta:
        unique_together = ('from_currency', 'to_currency',)
