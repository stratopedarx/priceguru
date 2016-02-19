# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20150704_2123'),
    ]

    operations = [
        migrations.RunSQL("""UPDATE "ItemPrice" SET currency='RUB' WHERE currency='RUR';""", None)
    ]
