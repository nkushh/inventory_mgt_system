# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-03 07:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_auto_20171003_1033'),
    ]

    operations = [
        migrations.AddField(
            model_name='item_supply',
            name='item_brand',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='item_supply',
            name='items_supplied',
            field=models.CharField(max_length=200),
        ),
    ]
