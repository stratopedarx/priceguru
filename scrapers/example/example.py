# -*- coding: utf-8 -*-
from core.api.decorators import autocomplete
import random
import string


def validate_url(url):
    return url


@autocomplete
def scrape(url):
    random_id = ''.join([
                            random.choice(string.ascii_letters + string.digits)
                            for i in xrange(16)
                            ])

    return dict(
        info=dict(
            title="Example title #%s" % random_id,
            article="Example article for #%s" % random_id,
            details="Example details for #%s" % random_id),
        price=dict(base_price=random.randint(0, 10000),
                   discount_price=random.randint(1, 10000))
    )
