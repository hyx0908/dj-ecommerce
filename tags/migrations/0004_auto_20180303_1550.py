# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-03-03 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_tag_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
