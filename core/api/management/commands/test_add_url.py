# -*- coding: utf-8 -*-
import json
from core.api.models import OriginalItem
from django.core.management import BaseCommand
from core.api.tasks import add_url


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '-id', '--id', nargs="+", type=int
        )

        parser.add_argument(
            '-url', '--url', nargs="+", type=str
        )

    def handle(self, *args, **options):
        id_list = []
        url_list = []

        if options['id'] is not None:
            id_list = options['id']

        if options['url'] is not None:
            url_list = options['url']

        for orig_item_obj in OriginalItem.objects.filter(id__in=id_list):
            print json.dumps(add_url(orig_item_obj.url), indent=4)

        for url in url_list:
            print json.dumps(add_url(url), indent=4)