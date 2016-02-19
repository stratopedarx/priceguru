# -*- coding: utf-8 -*

"""Ulmart scraper."""

from requests import Session
from lxml import html
 
ulmart_link = 'http://www.ulmart.ru/goods/3431156'
ulmart_link2 = 'http://www.ulmart.ru/goods/509798'
ulmart_link3 = 'http://discount.ulmart.ru/goods/3382091'
ulmart_link4 = 'http://www.ulmart.ru/goods/50'
 
 
def is_valid(page):
    """Validate the page."""
    return len(page.xpath('//span[@class="b-art__num"]/text()'))
 
 
def life_update(url):
    """Implement this in future."""
    return None


def get_page_info(link):
    """Make request to link url, parse results, return dict() with properties."""
    session = Session()
    res = session.get(link).text
    html_page = html.fromstring(res)
    if not is_valid(html_page):
        # this is not the final page
        print 'Page is not valid'
        return None
    parsed_data = parse_response(html_page)
    for key, value in parsed_data.iteritems():
        print u'{}: {}'.format(key, value)
    return parsed_data
 
 
def parse_response(page):
    """Parse given html page, return id, info, prices, available amount."""
    # price
    price_bar = page.xpath('//div[@class="b-product-card__price"]/span/span[@class="b-price__num"]/text()')[0]
    price = float(price_bar.replace(u'\xa0', ''))
    # discount
    discount_bar = page.xpath('//s[@class="b-price b-price_size5 b-price_old"]/span/text()')
    discount = None
    if len(discount_bar) > 0:
        old_price = float(discount_bar[0].replace(u'\xa0', ''))
        discount = old_price - price
    # no club price was found yet
    # TODO: prove that there's no club_price
    club_price = None
    # availability, currently implemented for predefined locale
    # TODO: add locale
    availability = get_availability(page)
 
    output = {
        'id': page.xpath('//span[@class="b-art__num"]/text()')[0],
        'name': page.xpath('//h1[@itemprop="name"]/text()')[0].lstrip().rstrip(),
        'info': page.xpath('//span[@itemprop="description"]/text()')[0].lstrip(),
        'price': price,
        'availability': availability,
    }
    if discount:
        output['discount'] = discount
    if club_price:
        output['club_price'] = club_price
    return output
 
 
def get_availability(page):
    """Get the availability of the good in the given city."""
    # TODO: implement locale
    # locale = page.xpath('//p[@class="navbar-text"]/span/text()')[0]
 
    availability = page.xpath('//div[@class="panel-body"]//div[@class="main-h5 h-box-title"]/text()')[0].rstrip()
    return availability != u'Нет в наличии'
 
