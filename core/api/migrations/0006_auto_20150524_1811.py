# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20150524_1734'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemgroup',
            unique_together=set([]),
        ),
    ]
