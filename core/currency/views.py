from core.currency.models import SupportedCurrency
from django.views.generic import RedirectView


class SetCurrencyView(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return self.request.GET.get("next", '/')

    def post(self, request):
        response = super(SetCurrencyView, self).post(request)
        ccy = request.POST.get("currency", None)
        if SupportedCurrency.objects.filter(code=ccy).exists():
            response.set_cookie('currency', ccy)
        return response