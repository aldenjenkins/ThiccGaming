# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-07-20 17:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobb_forum', '0002_auto_20170109_2035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ban',
            options={'verbose_name': 'Website-only Ban', 'verbose_name_plural': 'Website-only Bans'},
        ),
    ]
