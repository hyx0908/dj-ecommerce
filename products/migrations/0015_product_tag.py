# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-24 15:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0002_remove_tag_products'),
        ('products', '0014_product_timestamp'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tag',
            field=models.ManyToManyField(blank=True, to='tags.Tag'),
        ),
    ]
