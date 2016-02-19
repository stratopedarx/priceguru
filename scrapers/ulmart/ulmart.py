# -*- coding: utf-8 -*

"""Ulmart scraper."""
import re
import grab

from requests import Session
from lxml import html
from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url
 
ulmart_link = 'http://www.ulmart.ru/goods/3431156'
ulmart_link2 = 'http://www.ulmart.ru/goods/509798'
ulmart_link3 = 'http://discount.ulmart.ru/goods/3382091'
ulmart_link4 = 'http://www.ulmart.ru/goods/50'
 

def validate_url(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    session = Session()
    res = session.get(url).text
    page = html.fromstring(res)
    if page.xpath('//span[@class="b-art__num"]/text()'):
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, return info."""
    g = grab.Grab()
    g.go(url)
    parsed_data = parse_response(g)
    # discount_price = parsed_data['price'] - parsed_data['discount']
    price = dict(
        base_price=parsed_data['price'],
        discount_price=parsed_data['discount_price'],
    )
    info = dict(
        title=parsed_data['name'],
        article=parsed_data['id'],
        details=parsed_data['info'],
    )
    return dict(info=info, price=price)
 
 
def parse_response(page):
    """Parse given html page, return id, info, prices, available amount."""
    # price
    price_bar = page.doc.select('//div[@class="b-product-card__price"]/span/span[@class="b-price__num"]/text()').text()
    print price_bar, type(price_bar)
    price = float(re.sub(r'\s+', '', price_bar))
    # discount
    discount_bar = page.doc.select('//s[@class="b-price b-price_size5 b-price_old"]/span/text()').text_list()
    discount = 0
    if len(discount_bar) > 0:
        old_price = float(re.sub(r'\s+', '', discount_bar[0]))
        discount = price
        price = old_price
    # no club price was found yet
    # TODO: prove that there's no club_price
    club_price = 0
    # availability, currently implemented for predefined locale
    # TODO: add locale
    availability = get_availability(page)
 
    output = {
        'id': page.doc.select('//span[@class="b-art__num"]/text()').text(),
        'name': page.doc.select('//h1[@itemprop="name"]/text()').text().lstrip().rstrip(),
        'info': page.doc.select('//span[@itemprop="description"]/text()').text().lstrip(),
        'price': price,
        'availability': availability,
        'discount_price': discount,
        'club_price': club_price,
    }
    return output
 
 
def get_availability(page):
    """Get the availability of the good in the given city."""
    # TODO: implement locale
    # locale = page.xpath('//p[@class="navbar-text"]/span/text()')[0]
 
    availability = page.xpath('//div[@class="panel panel-default"]//div[@class="main-h5 h-box-title"]/text()')[0].rstrip()
    return availability != u'Нет в наличии'
