# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2017-01-13 19:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20170112_1923'),
    ]

    operations = [
        migrations.RenameField(
            model_name='classesdate',
            old_name='group',
            new_name='classes',
        ),
    ]