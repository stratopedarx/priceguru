# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_merge'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='itemgroup',
            unique_together=set([('user', 'group_name')]),
        ),
    ]
