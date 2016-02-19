# -*- coding: utf-8 -*-

def autocomplete(func):
    def __callback__(url):
        data = func(url)
        return dict(
            url=url,
            data=data
        )
    return __callback__
