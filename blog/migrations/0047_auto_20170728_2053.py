# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-28 17:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0046_auto_20170728_0912'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='is_active',
            field=models.CharField(default=1, max_length=1, verbose_name='1-активний, 0-неактивний'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='default8.png', null=True, upload_to='user_avatar'),
        ),
    ]