"""Citilink scraper."""

from re import findall
from requests import Session
from lxml import html
 
citilink_link = 'http://www.citilink.ru/catalog/photo_and_video/photo_filters/685070/'
citilink_link2 = 'http://www.citilink.ru/catalog/computers_and_notebooks/gift_certificates/554178/'
citilink_link3 = 'http://www.citilink.ru/catalog/large_and_small_appliances/small_appliances/kettles/991346/'
citilink_link4 = 'http://www.citilink.ru/catalog/mobile/notebooks/956633/'
 
 
def is_valid(page):
    """Validate the page."""
    return len(page.xpath('//div[@id="item_new"]/span/text()'))
 
 
def life_update(url):
    """Implement this in future."""
    return None


def get_page_info(link):
    """Make request to link url, parse results"""
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
    good_id = page.xpath('//div[@id="item_new"]/span/text()')[0]
    name = page.xpath('//div[@id="item_new"]/h1/text()')[0]
    info_bar = page.xpath('//div[@class="orange info"]/p/text()')
    if info_bar:
        info = info_bar[0].lstrip()
    else:
        info = 'no info'
    # discount
    discount = None
    discount_bar = page.xpath('//td[@class="price-blck"]/*[@class="discountSell"]/text()')
    if len(discount_bar) > 0:
        discount = float(findall('(\d+)', discount_bar[0])[0])
    # price
    price_bar = page.xpath('//td[@class="price-blck"]/div/span/text()')
    if price_bar:
        price = float(price_bar[0].replace(' ', '').replace(',', '.'))
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = False       
 
    club_price_bar = page.xpath('//td[@class="price-blck"]/div[@class="price club_price"]/text()')
    club_price = float(club_price_bar[0][:-1].replace(' ', '').replace(',', '.')) if len(club_price_bar) > 0 else None
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
    Get the availability of the good in the given city
 
    parsed from image names
    """
    # TODO: implement locale
    amount = 0
    availability = page.xpath('//div[@class="grey"]//td[@align="right"]')[0]
    for place in availability.getchildren():
        amount += int(findall('/avail_(\d*).png', place.xpath('.//img/@src')[0])[0])
    return True if amount else False
