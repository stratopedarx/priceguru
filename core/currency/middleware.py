# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect


class CurrencyMiddleware(object):
    def process_request(self, request):
        if request.COOKIES.get("currency", None) is None:
            response = HttpResponseRedirect(request.build_absolute_uri())
            response.set_cookie("currency", "RUB", 8600)
            return response
