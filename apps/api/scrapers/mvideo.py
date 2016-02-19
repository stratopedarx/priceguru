# -*- coding: utf-8 -*

"""Mvideo scraper."""
 
from requests import Session
from lxml import html
 
mvideo_link = 'http://www.mvideo.ru/products/dvd-disk-media-avatar-40054563#shopdirections'
mvideo_link2 = 'http://www.mvideo.ru/products/televizor-philips-55pfs8159-60-10007415'
mvideo_link3 = 'http://www.mvideo.ru/products/videoproektor-multimediinyi-acer-p1500-10005039'
mvideo_link4 = 'http://www.mvideo.ru/products/smartfon-apple-iphone-5c-8gb-yellow-mg8y2ru-a-30020700?horiz&cityId=CityCZ_974'
 
 
def is_valid(page):
    """Validate the page."""
    return len(page.xpath('//div[@class="product-data-rating-code"]/p'))
 
 
def life_update(url):
    """Implement this in future."""
    return None


def get_page_info(link):
    """Make request to link url, parse results."""
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
    good_id = page.xpath('.//div[@class="product-data-rating-code"]/p/text()')[0].split()[-1]
    name = page.xpath('.//h1[@class="product-title"]/text()')[0].strip()
    info = ''
    for td in page.xpath('.//table[@class="table table-striped product-details-table"]/tbody')[0]:
        property_key_bar = td.xpath('./td[1]/text()')
        property_key = property_key_bar[0] if property_key_bar else ''
        property_value_bar = td.xpath('./td[2]/text()')
        property_value = property_value_bar[0] if property_value_bar else ''
        info += property_key + ' - ' + property_value + '; '
    # discount
    discount = None
    discount_bar = page.xpath(
        './/div[@class="product-details-summary-economy-info highlighted-text-primary pull-right"]/text()'
    )
    if len(discount_bar) > 0:
        discount = float(discount_bar[0])
    # price
    price_bar = page.xpath('.//strong[@class="product-price-current"]/text()')
    if price_bar:
        price = float(page.xpath('.//strong[@class="product-price-current"]/text()')[0])
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = 0
    # TODO: prove that there's no club_price
    club_price = None
    # availability, currently implemented for predefined locale
    # TODO: add locale
 
    output = {
        'id': good_id,
        'name': name,
        'info': info,
        'price': price,
        'availability': availability,
    }
    if discount:
        output['discount'] = discount
    if club_price:
        output['club_price'] = club_price
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
