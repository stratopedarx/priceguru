# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import core.api.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=64, verbose_name='Group name')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'ItemGroup',
                'verbose_name': 'Item group',
                'verbose_name_plural': 'Item groups',
            },
        ),
        migrations.CreateModel(
            name='ItemPrice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('base_price', models.FloatField(default=0)),
                ('discount_price', models.FloatField(default=0)),
                ('current_price', models.FloatField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('currency', models.CharField(default=b'RUR', max_length=8)),
            ],
            options={
                'db_table': 'ItemPrice',
                'verbose_name': 'Item price',
                'verbose_name_plural': 'Item prices',
            },
        ),
        migrations.CreateModel(
            name='OriginalItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('article', models.CharField(max_length=255, null=True, blank=True)),
                ('title', models.CharField(max_length=255)),
                ('details', models.TextField()),
                ('url', models.URLField(max_length=1024, db_index=True)),
            ],
            options={
                'db_table': 'OriginalItem',
                'verbose_name': 'Original Item',
                'verbose_name_plural': 'Original Items',
            },
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='Partner name')),
                ('package', models.CharField(help_text='^[a-zA-z]\\w+$', max_length=16, verbose_name='Source package', validators=[core.api.models.check_valid_package])),
            ],
            options={
                'db_table': 'Partner',
                'verbose_name': 'Partner',
                'verbose_name_plural': 'Partners',
            },
        ),
        migrations.CreateModel(
            name='PartnerSource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(help_text='www.example.com', max_length=64)),
                ('scraper_name', models.CharField(help_text='scrapers.package.(^[a-zA-z]\\w+$)', max_length=16, validators=[core.api.models.check_valid_package])),
                ('platform', models.CharField(max_length=64, verbose_name='Platform')),
                ('partner', models.ForeignKey(to='api.Partner')),
            ],
            options={
                'db_table': 'PartnerSource',
                'verbose_name': 'Partner Source',
                'verbose_name_plural': 'Partners Sources',
            },
        ),
        migrations.CreateModel(
            name='UserItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('custom_name', models.CharField(max_length=255)),
                ('group', models.ForeignKey(to='api.ItemGroup')),
                ('item', models.ForeignKey(to='api.OriginalItem')),
            ],
            options={
                'db_table': 'UserItem',
                'verbose_name': 'User item',
                'verbose_name_plural': 'User items',
            },
        ),
        migrations.AddField(
            model_name='originalitem',
            name='source',
            field=models.ForeignKey(to='api.PartnerSource'),
        ),
        migrations.AddField(
            model_name='itemprice',
            name='item',
            field=models.ForeignKey(to='api.OriginalItem'),
        ),
        migrations.AlterUniqueTogether(
            name='useritem',
            unique_together=set([('item', 'group')]),
        ),
    ]
