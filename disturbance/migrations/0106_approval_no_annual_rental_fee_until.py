# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-07-08 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0105_auto_20200707_1038'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='no_annual_rental_fee_until',
            field=models.DateField(blank=True, null=True),
        ),
    ]
