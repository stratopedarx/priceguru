# -*- coding: utf-8 -*-
import urlparse
import urllib
from collections import OrderedDict


def clean_url(url, path=True, params=True, query=True, fragment=True):
    url = urlparse.urlparse(url)
    return urlparse.ParseResult(
        url.scheme,
        url.netloc,
        url.path if path else "",
        url.params if params else "",
        url.query if query else "",
        url.fragment if fragment else "",
    ).geturl()


def clean_query(url, *args):
    """
    query keys will be sorted in result.

    :param url: basestring
    :param args: list
    :return: string
    """
    url_parsed = urlparse.urlparse(url)
    query_dict = OrderedDict(urlparse.parse_qsl(url_parsed.query))
    for key in query_dict.keys():
        if key not in args:
            query_dict.pop(key, None)
    query_string = urllib.urlencode(query_dict)
    return urlparse.ParseResult(
        url_parsed.scheme,
        url_parsed.netloc,
        url_parsed.path,
        url_parsed.params,
        query_string,
        url_parsed.fragment
    ).geturl()
