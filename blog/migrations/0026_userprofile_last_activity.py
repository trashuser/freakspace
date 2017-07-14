# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-05 06:40
from __future__ import unicode_literals

from django.db import migrations, models
import time


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0025_remove_userprofile_last_activity'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='last_activity',
            field=models.IntegerField(default=time.time, verbose_name='Остання активність'),
        ),
    ]