# coding: utf-8

"""Citilink scraper."""

import grab
import re

from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url


def validate_url(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    g = grab.Grab()
    _change_city(g)

    g.go(url)
    if g.doc.select('//ul[contains(@class,"product_info_switcher")]').exists():
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, parse results."""
    g = grab.Grab()
    _change_city(g)

    g.go(url)
    parsed_data = _parse_response(g.doc)

    discount_price = parsed_data['price'] - parsed_data['discount']
    price = dict(
        base_price=parsed_data['price'],
        discount_price=discount_price,
    )
    info = dict(
        title=parsed_data['name'],
        article=parsed_data['id'],
        details=parsed_data['info'],
    )
    return dict(info=info, price=price)


def _change_city(g):
    """Change city to the user's. Should be implemented."""
    # TODO: implement
    city_url = 'http://www.citilink.ru/?action=changeCity&space_id=nnov_cl'  # Nizhny Novgorod
    g.go(city_url)


def _parse_response(page):
    """Parse given html page, return id, info, prices, available amount."""
    good_id = page.select('//span[@class="product_id"]').text()
    name = page.select('//div[@class="product_header"]/h1').text()

    info_el = page.select('//p[@class="short_description"]')
    info = info_el.text().strip() if info_el.exists() else 'no info'

    price_el = page.select('//tr[@class="standart_price"]//span[@class="price"]/ins[@class="num"]')
    if price_el.exists():
        price = float(price_el.text().replace(' ', '').replace(',', '.'))
        availability = _get_availability(page)
    else:
        price = 0
        availability = False  # price is missing = no such a good in the market

    # missing on the good's page
    discount = 0
    club_price = 0

    output = {
        'id': good_id,
        'name': name,
        'info': info,
        'price': price,
        'availability': availability,
        'discount': discount,
        'club_price': club_price,
    }
    return output


def _get_availability(page):
    """Get the availability of the good in the given city parsed from image names."""
    text_values = {
        u'нет': 0,
        u'много': 10,
    }

    amount = 0
    place_els = page.select('//div[@class="in_stock_vertical_position"]//td[@class="few"]')
    for place_el in place_els:
        text = place_el.text().strip()
        if text in text_values:
            amount += text_values[text]
        else:
            amount += int(re.findall(r'^(\d+)[^d]*$', text)[0])

    return (amount > 0)


"""
links:
http://www.citilink.ru/catalog/photo_and_video/photo_filters/685070/
http://www.citilink.ru/catalog/computers_and_notebooks/gift_certificates/554178/
http://www.citilink.ru/catalog/large_and_small_appliances/small_appliances/kettles/991346/
http://www.citilink.ru/catalog/mobile/notebooks/956633/
"""
