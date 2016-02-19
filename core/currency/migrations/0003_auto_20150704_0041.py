# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0002_function_get_currency_ratio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyratio',
            name='ratio',
            field=models.FloatField(default=1.0),
        ),
    ]
