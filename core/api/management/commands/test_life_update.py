# -*- coding: utf-8 -*-
import json
from core.api.models import OriginalItem
from django.core.management import BaseCommand
from core.api.tasks import life_update


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

        for item in OriginalItem.objects.filter(id__in=id_list):
            print json.dumps(life_update(item.url), indent=4)

        for url in url_list:
            print json.dumps(life_update(url), indent=4)
