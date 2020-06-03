# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2020-05-20 07:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disturbance', '0053_auto_20200520_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeedPollDocument',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('uploaded_date', models.DateTimeField(auto_now_add=True)),
                ('input_name', models.CharField(blank=True, max_length=255, null=True)),
                ('can_delete', models.BooleanField(default=True)),
                ('visible', models.BooleanField(default=True)),
                ('_file', models.FileField(max_length=512, upload_to=b'')),
                ('proposal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deed_poll_documents', to='disturbance.Proposal')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='apiarysite',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disturbance.District'),
        ),
        migrations.AddField(
            model_name='apiarysite',
            name='region',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='disturbance.Region'),
        ),
    ]