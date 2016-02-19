# -*- coding: utf-8 -*

"""Mvideo scraper."""
import grab

from requests import Session
from lxml import html
from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url
 
mvideo_link = 'http://www.mvideo.ru/products/dvd-disk-media-avatar-40054563#shopdirections'
mvideo_link2 = 'http://www.mvideo.ru/products/televizor-philips-55pfs8159-60-10007415'
mvideo_link3 = 'http://www.mvideo.ru/products/videoproektor-multimediinyi-acer-p1500-10005039'
mvideo_link4 = 'http://www.mvideo.ru/products/smartfon-apple-iphone-5c-8gb-yellow-mg8y2ru-a-30020700?horiz&cityId=CityCZ_974'


def validate_url(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    session = Session()
    res = session.get(url).text
    page = html.fromstring(res)
    if page.xpath('//div[@class="product-data-rating-code"]/p'):
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, parse results."""
    g = grab.Grab()
    g.go(url)
    parsed_data = parse_response(g)
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
 
 
def parse_response(page):
    """Parse given html page, return id, info, prices, available amount."""
    good_id = page.doc.select('.//div[@class="product-data-rating-code"]/p/text()').text().split()[-1]
    name = page.doc.select('.//h1[@class="product-title"]/text()').text().strip()
    info = ''
    for elem in page.xpath('.//table[@class="table table-striped product-details-table"]'):
        property_key_bar = elem.xpath('./td[1]/text()')
        property_key = property_key_bar[0] if property_key_bar else ''
        property_value_bar = elem.xpath('./td[2]/text()')
        property_value = property_value_bar[0] if property_value_bar else ''
        info += property_key + ' - ' + property_value + '; '
    # discount
    discount = 0
    discount_bar = page.doc.select(
        './/div[@class="product-details-summary-economy-info highlighted-text-primary pull-right"]/text()'
    ).text_list()
    if len(discount_bar) > 0:
        discount = float(discount_bar[0])
    # price
    price_bar = page.doc.select('.//strong[@class="product-price-current"]/text()').text()
    if price_bar:
        price = float(page.doc.select('.//strong[@class="product-price-current"]/text()').text())
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = 0
    # TODO: prove that there's no club_price
    club_price = 0
    # availability, currently implemented for predefined locale
    # TODO: add locale
 
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
 
 
def get_availability(page):
    """
    Get the availability of the good in the given city.
 
    Parsed from <script> tag, which contains main info about the good.
    """
    # TODO: implement locale
 
    properties = page.xpath('//body[@class="productDetails no-inner-shaddow"]/script/text()')[0]
    availability = properties.find("'productAvailability': 'available'")
    return True if availability > -1 else False
