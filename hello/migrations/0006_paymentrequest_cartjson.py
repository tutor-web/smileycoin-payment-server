# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-19 10:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0005_auto_20160819_0952'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='cartJSON',
            field=models.CharField(default='{}', max_length=300),
            preserve_default=False,
        ),
    ]
