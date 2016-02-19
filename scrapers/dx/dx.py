"""Dx.com scraper."""

from requests import Session
from lxml import html
from core.api.decorators import autocomplete
from core.api.exceptions import InvalidDeepLink
from core.api.functions import clean_url


dx_link = 'http://www.dx.com/en/p/uk-type-travel-charger-power-adapter-for-nokia-6230-3310-180-240v-47766'


def validate_url(url):
    """Check if the page is final. Bad code, should be parsed here."""
    # TODO: remove parsing from here
    session = Session()
    res = session.get(url).text
    page = html.fromstring(res)
    if page.xpath('//span[@class="product_sku"]/span[@id="sku"]/text()'):
        return clean_url(url, fragment=False, query=False, params=False)
    raise InvalidDeepLink(url)


@autocomplete
def scrape(url):
    """Make request to link url, parse results"""
    session = Session()
    res = session.get(url).text
    html_page = html.fromstring(res)
    parsed_data = parse_response(html_page)
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
    good_id = page.xpath('//span[@class="product_sku"]/span[@id="sku"]/text()')[0]
    name = page.xpath('//span[@itemprop="name"]/text()')[0]
    params = page.xpath(
        '//div[@id="overview-detailinfo"]/div/table/tr')
    info = ','.join([
        u'{k} - {v}'.format(
            k=param.xpath('./td/strong/text()')[0],
            v=param.xpath('./td/text()')[0])
        for param in params
    ])

    # price
    price_bar = page.xpath('//span[@id="price"]/text()')
    if price_bar:
        price = float(price_bar[0].replace(",", "."))
        availability = get_availability(page)
    else:
        # price is missing = no such a good in the market
        price = 0
        availability = False

    # discount
    discount_price = 0
    before_discount_price_bar = page.xpath('//div[@class="lp "]/span[@id="list-price"]/text()')
    if before_discount_price_bar:
        before_discount_price = float(before_discount_price_bar[0][3:].replace(",", "."))
        discount_price = price
        price = before_discount_price

    club_price = 0

    output = {
        'id': good_id,
        'name': name,
        'info': info,
        'price': price,
        'availability': availability,
        'discount_price': discount_price,
        'club_price': club_price,
    }
    return output


def get_availability(page):
    """
    Get the availability of the good in the given city

    parsed from image names
    """
    storage_info_bar = page.xpath('//span[@class="storage_info "]/strong/text()')
    if storage_info_bar and storage_info_bar[0] == 'Sold out':
        return False
    return True
