# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, max_length=32)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=32, null=True, blank=True)),
                ('last_name', models.CharField(max_length=32, null=True, blank=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
