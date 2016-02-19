"""Aliexpress scraper."""
# TODO: remove parsing from here

from re import findall
from requests import Session
from lxml import html
from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url
 
aliexpress_link = 'http://ru.aliexpress.com/item/High-Quality-Car-Audio-Stereo-In-Dash-Auto-Car-Radio-MP3-Player-FM-Aux-Input-Receiver/32321806763.html'
aliexpress_link2 = 'http://ru.aliexpress.com/item/OEM-VW-RCD510-Radio-For-VW-Volkswagen-with-USB-Cable-Code-Support-RVC-OPS-iPod-Bluetooth/1742153857.html'
aliexpress_link3 = 'http://ru.aliexpress.com/item/Scholl-Set-Velvet-Smooth-Express-Pedi-2-Replacement-Roller-Heads-Foot-Care-Tool-Free-shipping/32303347626.html'
aliexpress_link4 = 'http://ru.aliexpress.com/item/New-Hot-sales-Stainless-Steel-Handle-High-Elastic-Rubber-Catapult-Slingshot-Pro-Outdoor-Game-Best-Gift/32255933785.html'
 

def is_valid(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    session = Session()
    res = session.get(url).text
    page = html.fromstring(res)
    if page.xpath('//div[@class="col-sub"]/div[@class="prod-id"]/span/text()') != []:
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, return info."""
    session = Session()
    res = session.get(url).text
    html_page = html.fromstring(res)
    parsed_data = parse_response(html_page)
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
    good_id = page.xpath('//div[@class="col-sub"]/div[@class="prod-id"]/span/text()')[0].split()[2]
    name = page.xpath('//h1[@class="product-name"]/text()')[0]
    params = page.xpath(
        '//div[@class="ui-box ui-box-normal product-params"]/div[@class="ui-box-body"]/dl')
    info = ','.join([u'{dt} - {dd}'.format(
        dt=param.xpath('./dt/text()')[0],
        dd=param.xpath('./dd/text()')[0])
        for param in params
    ])

    # price
    price_bar = page.xpath('//span[@id="sku-price"]/text()')
    if price_bar:
        price = float(price_bar[0].replace(u'\xa0', '').replace(',' ,'.'))
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = False

    # discount
    discount = 0
    discount_price_bar = page.xpath('//span[@id="sku-discount-price"]/text()')
    if discount_price_bar:
        discount_price = float(discount_price_bar[0].replace(u'\xa0', '').replace(',' ,'.'))
        discount = price - discount_price

    # here's no club price but we can get bulk-price(do we need this?)
    club_price = 0
 
    output = {
        'id': good_id,
        'name': name,
        'info': info,
        'price': price,
        'availability': availability,
        'discount': discount,
        'club_price' : club_price,
    }
    return output
 
 
def get_availability(page):
    """Get the availability of the good."""
    product_info = page.xpath('//div[@class="product-info"]/form/script/text()')[0]
    amount = findall('<span id="quantity-no">(\d+)</span>', product_info)
    if amount and int(amount[0]) > 0:
        print 'availability = {amount}'.format(amount=amount[0])
        return True
    return False
