# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-22 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20161022_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='stationary',
            field=models.BooleanField(choices=[(True, 'stacjonarne'), (False, 'niestacjonarne')], default=True),
        ),
    ]
