# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-28 16:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture_sharing', '0002_auto_20160928_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='date_last_view',
            field=models.DateTimeField(null=True),
        ),
    ]
