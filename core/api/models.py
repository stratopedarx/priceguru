# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
import re


def check_valid_package(value):
    return bool(re.match("^[a-zA-Z]\w+$", value))


class Partner(models.Model):
    """
    Model for partner basic description
    """
    name = models.CharField(max_length=64, verbose_name=_('Partner name'))
    package = models.CharField(max_length=16,
                               validators=[check_valid_package],
                               verbose_name=_("Source package"),
                               help_text=_("^[a-zA-z]\w+$"))

    def __unicode__(self):
        return self.name

    class Meta: 
        db_table = u'Partner'
        verbose_name = _(u'Partner')
        verbose_name_plural = _(u'Partners')


class PartnerSource(models.Model):
    """
    Model for 3d parties sources, each partner may have mobile/desktop version etc
    """
    partner = models.ForeignKey(Partner)
    domain = models.CharField(max_length=64,
                              help_text=_("www.example.com"))

    scraper_name = models.CharField(max_length=16,
                                    validators=[check_valid_package],
                                    help_text=_("scrapers.package.(^[a-zA-z]\w+$)")
                                    )

    # TODO: Further might be reasonable to change platform to ChoiceField
    platform = models.CharField(max_length=64, verbose_name=u'Platform')

    def __unicode__(self):
        return self.domain

    class Meta:
        db_table = u'PartnerSource'
        verbose_name = _(u'Partner Source')
        verbose_name_plural = _(u'Partners Sources')


class OriginalItem(models.Model):
    """
    Model for items originally described on 3d party side
    """
    # Item number in 3d party database. It can be empty
    article = models.CharField(max_length=255,
                               blank=True,
                               null=True)
    # How item is called on 3d party site
    title = models.CharField(max_length=255)
    # Description of item on the 3d party side
    details = models.TextField()

    # URL link to final page with all details
    url = models.URLField(max_length=1024,
                          db_index=True,
                          null=False,
                          unique=True)

    source = models.ForeignKey(PartnerSource)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = u'OriginalItem'
        verbose_name = _(u'Original Item')
        verbose_name_plural = _(u'Original Items')


class ItemGroup(models.Model):
    """
    Model for group of Items Customized by User
    """
    # TODO: investigate on practise is it necessary to keep group_name or generate it like 'group128474_user-huyuser'
    group_name = models.CharField(max_length=64,
                                  verbose_name=_("Group name"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.group_name

    class Meta:
        db_table = u'ItemGroup'
        verbose_name = _(u'Item group')
        verbose_name_plural = _(u'Item groups')
        unique_together = ('user', 'group_name')



class UserItem(models.Model):
    """
    Model for items in User Group
    """
    custom_name = models.CharField(max_length=255,
                                   blank=False,
                                   null=False)
    item = models.ForeignKey(OriginalItem)
    group = models.ForeignKey(ItemGroup)

    def __unicode__(self):
        return self.custom_name

    class Meta:
        db_table = u'UserItem'
        verbose_name = _(u'User item')
        verbose_name_plural = _(u'User items')
        unique_together = ('item', 'group')


class ItemPrice(models.Model):
    """
    Model for item's prices including information about last date of update, current price
    """
    item = models.ForeignKey(OriginalItem)
    base_price = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    current_price = models.FloatField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    currency = models.CharField(max_length=8,
                                default="RUB")

    def __unicode__(self):
        return u"%(item)s %(current_price)s %(currency)s" % {'item': self.item,
                                                             'current_price': self.current_price,
                                                             'currency': self.currency}

    class Meta:
        db_table = u'ItemPrice'
        verbose_name = _(u'Item price')
        verbose_name_plural = _(u'Item prices')
