# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-17 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_classes_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='short_name',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
    ]
