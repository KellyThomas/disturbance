# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-08-18 06:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0130_auto_20200817_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apiaryglobalsettings',
            name='_file',
            field=models.FileField(blank=True, null=True, upload_to='apiary_licence_template'),
        ),
    ]
