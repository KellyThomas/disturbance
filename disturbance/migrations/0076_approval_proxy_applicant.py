# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-06-12 03:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('disturbance', '0075_auto_20200609_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='proxy_applicant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='proxy_approvals', to=settings.AUTH_USER_MODEL),
        ),
    ]
