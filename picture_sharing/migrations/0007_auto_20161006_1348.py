# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-06 10:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('picture_sharing', '0006_auto_20161003_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
