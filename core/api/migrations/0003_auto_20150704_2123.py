# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20150601_1446'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemprice',
            name='currency',
            field=models.CharField(default=b'RUB', max_length=8),
        ),
    ]
