# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-03 06:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bpay', '0008_auto_20170203_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='BillerCodeRecipient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='BillerCodeSystem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('biller_code', models.CharField(max_length=10, unique=True)),
                ('system', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='billercoderecipient',
            name='app',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bpay.BillerCodeSystem'),
        ),
    ]
