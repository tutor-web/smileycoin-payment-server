# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-08-22 14:11
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0008_paymentrequest_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymentrequest',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2016, 8, 22, 14, 11, 35, 672551, tzinfo=utc), verbose_name=b'date created'),
            preserve_default=False,
        ),
    ]