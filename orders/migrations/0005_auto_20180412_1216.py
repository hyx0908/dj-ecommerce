# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-12 10:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_auto_20180411_1242'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ['-timestamp']},
        ),
    ]