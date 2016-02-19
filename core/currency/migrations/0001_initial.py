# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CurrencyRatio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_currency', models.CharField(max_length=3)),
                ('to_currency', models.CharField(max_length=3)),
                ('ratio', models.FloatField()),
                ('updated_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupportedCurrency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=3)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='currencyratio',
            unique_together=set([('from_currency', 'to_currency')]),
        ),
    ]
