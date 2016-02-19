# -*- coding: utf-8 -*-
from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("--package", "-p", type=str, required=True,
                            help='put here package name scrapers.(package.module).scrape(url)')
        parser.add_argument("--module", "-m", type=str, required=True,
                            help='put here module name scrapers.(package.module).scrape(url)')
        parser.add_argument("--url", "-u", type=str, nargs="+", required=True,
                            help='put here urls list for scraper')

    def handle(self, *args, **options):
        scraper = __import__("scrapers.{o[package]}.{o[module]}".format(o=options),
                         fromlist=['scrapers.{o[package]}'.format(o=options)])

        for url in options['url']:
            cleaned_url = scraper.validate_url(url)
            print scraper.scrape(cleaned_url)
            print "=" * 80