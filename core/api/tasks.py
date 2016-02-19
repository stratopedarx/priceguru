# -*- coding: utf-8 -*-
import json
import urlparse
from datetime import timedelta
from celery.task import periodic_task
from core.api.exceptions import WebsiteNotImplemented
from django.core import serializers
from django.utils.timezone import utc
from django.template import defaultfilters
from models import PartnerSource, OriginalItem, ItemPrice, UserItem
from celery import shared_task, group

import grab
import grab.error
import traceback

import logging

log = logging.getLogger('file')


def to_json_handler(func):
    def __callback__(*args, **kwargs):
        error = None
        result = None
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            error = dict(
                name=getattr(e, "__name__", getattr(e.__class__, "__name__")),
                traceback=traceback.format_exc()
            )
        return dict(
            success=not error,
            result=result,
            error=error
        )

    return __callback__

# reuse code
def validate(url):
    # g = grab.Grab()
    # g.go(url)
    # actual_url = g.response.url
    domain = urlparse.urlparse(url).netloc
    if PartnerSource.objects.filter(domain=domain).exists():
        source_obj = PartnerSource.objects.get(domain=domain)
    else:
        raise WebsiteNotImplemented

    scraper = __import__("scrapers.{obj.partner.package}.{obj.scraper_name}".format(obj=source_obj),
                         fromlist=['scrapers.{obj.partner.package}'.format(obj=source_obj)])
    cleaned_url = scraper.validate_url(url)
    return source_obj, scraper, cleaned_url





@shared_task(name='core.api.tasks.add_url')
@to_json_handler
def add_url(url):
    source_obj, scraper, url = validate(url)
    try:
        item = OriginalItem.objects.get(url=url)
        result = scraper.scrape(url)
    except Exception as e:
        result = scraper.scrape(url)
        result['data']['info']['url'] = result['url']
        item = OriginalItem(source=source_obj, **result['data']['info'])
        item.save()

    tpl_data = dict(
        base_price=0.0,
        discount_price=00
    )
    tpl_data.update(result['data']['price'])

    item_price = ItemPrice(
        item=item,
        current_price=min(filter(lambda x: x > 0, tpl_data.values()) or (0.0,)),
        **tpl_data
    )
    item_price.save()

    item = json.loads(serializers.serialize("json", [item]))[0]
    price = json.loads(serializers.serialize("json", [item_price]))[0]
    return dict(item=item, price=price)


@shared_task(name='core.api.tasks.add_useritem_into_group')
@to_json_handler
def add_useritem_into_group(url, group_id):
    source_obj, scraper, url = validate(url)
    try:
        item = OriginalItem.objects.get(url=url)
        result = scraper.scrape(url)
    except Exception as e:
        result = scraper.scrape(url)
        result['data']['info']['url'] = result['url']
        item = OriginalItem(source=source_obj, **result['data']['info'])
        item.save()

    tpl_data = dict(
        base_price=0.0,
        discount_price=00
    )
    tpl_data.update(result['data']['price'])

    item_price = ItemPrice(
        item=item,
        current_price=min(filter(lambda x: x > 0, tpl_data.values()) or (0.0,)),
        **tpl_data
    )
    item_price.save()

    user_item = UserItem.objects.create(group_id=group_id, item=item, custom_name=item.title)
    partner = item.source.partner

    item_price.current_price = defaultfilters.floatformat(item_price.current_price, 2)
    item = json.loads(serializers.serialize("json", [item]))[0]
    price = json.loads(serializers.serialize("json", [item_price]))[0]
    user_item = json.loads(serializers.serialize('json', [user_item]))[0]
    partner = json.loads(serializers.serialize('json', [partner]))[0]
    price['formatted_date'] = defaultfilters.date(item_price.created_date.replace(tzinfo=utc), u"d E Y г. H:i")

    return dict(item=item, price=price, user_item=user_item, partner=partner)


@periodic_task(run_every=timedelta(minutes=15))
def live_update_all():
    to_update = OriginalItem.objects.raw("""
select "OriginalItem"."id",
       "OriginalItem"."url"
from "OriginalItem"
        left join "ItemPrice" on "OriginalItem"."id"="ItemPrice"."item_id" and "ItemPrice"."created_date" >= now() - interval '2 hours'
where "ItemPrice"."created_date" is null;
    """)
    urls = [o_item.url for o_item in to_update]
    if urls:
        result = group(map(lambda url: add_url.s(url), urls)).apply()
        while not result.ready():
            pass
        log.debug(json.dumps([i.result for i in result]))
