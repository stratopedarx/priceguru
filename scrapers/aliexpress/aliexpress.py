"""Aliexpress scraper."""
# TODO: remove parsing from here
import re
import grab

from re import findall
from requests import Session
from lxml import html
from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url
 
aliexpress_link = 'http://ru.aliexpress.com/item/High-Quality-Car-Audio-Stereo-In-Dash-Auto-Car-Radio-MP3-Player-FM-Aux-Input-Receiver/32321806763.html'
aliexpress_link2 = 'http://ru.aliexpress.com/item/2015-Hot-Women-Sexy-Summer-Boho-Long-Maxi-Evening-Party-Dress-Beach-Long-Dress/32367515166.html'
aliexpress_link3 = 'http://ru.aliexpress.com/item/Scholl-Set-Velvet-Smooth-Express-Pedi-2-Replacement-Roller-Heads-Foot-Care-Tool-Free-shipping/32303347626.html'
aliexpress_link4 = 'http://ru.aliexpress.com/item/New-Hot-sales-Stainless-Steel-Handle-High-Elastic-Rubber-Catapult-Slingshot-Pro-Outdoor-Game-Best-Gift/32255933785.html'
 

def validate_url(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    g = grab.Grab()
    g.go(url)
    if g.doc.select('//div[@class="col-sub"]/div[@class="prod-id"]/span/text()').text():
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, return info."""
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
    good_id = page.doc.select('//div[@class="col-sub"]/div[@class="prod-id"]/span/text()').text().split()[2]
    name = page.doc.select('//h1[@class="product-name"]/text()').text()
    params = page.doc.select('//div[@class="ui-box ui-box-normal product-params"]/div[@class="ui-box-body"]/dl')
    info = ','.join([u'{dt} - {dd}'.format(
        dt=param.select('./dt/text()').text(),
        dd=param.select('./dd/text()').text())
        for param in params
    ])

    # price
    price_bar = page.doc.select('//span[@id="sku-price"]/text()').text_list()
    if price_bar:
        price_raw = re.sub(r'\s+', '', price_bar[0]).replace(',', '.')
        # sometimes it has weird format 'price1 - price2':
        if '-' in price_raw:
            price = float(price_raw.split('-')[0])
        else:
            price = float(price_raw)
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = False

    # discount
    discount = 0
    discount_price_bar = page.doc.select('//span[@id="sku-discount-price"]/text()').text_list()
    if discount_price_bar:
        discount_price_raw = discount_price_bar[0].replace(u'\xa0', '').replace(',', '.')
        # when price is 'price1-price2':
        if '-' in discount_price_raw:
            discount_price_raw = page.doc.select(
                '//span[@id="sku-discount-price"]/span[@itemprop="lowPrice"]/text()'
            ).text().replace(u'\xa0', '').replace(',', '.')
        discount_price = float(discount_price_raw)
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
        'club_price': club_price,
    }
    return output
 
 
def get_availability(page):
    """Get the availability of the good."""
    product_info = page.doc.select('//div[@class="product-info"]/form/script/text()').text()
    amount = findall('<span id="quantity-no">(\d+)</span>', product_info)
    if amount and int(amount[0]) > 0:
        print 'availability = {amount}'.format(amount=amount[0])
        return True
    return False
