# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 11:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture_sharing', '0008_auto_20161006_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='user',
            field=models.CharField(default='anonymous', max_length=20),
        ),
    ]