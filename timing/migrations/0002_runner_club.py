# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-03-24 09:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='runner',
            name='club',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Club'),
        ),
    ]
