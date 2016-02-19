# -*- coding: utf-8 -*-
from datetime import timedelta
from core.api.models import OriginalItem, ItemPrice, ItemGroup, UserItem
from django.utils.timezone import now
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['group_list'] = ItemGroup.objects.order_by("?")[:3]
        return context