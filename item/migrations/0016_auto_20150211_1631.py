# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_auto_20150211_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='getmoney',
            name='money',
            field=models.IntegerField(default=0, max_length=10, verbose_name=b'money_for_user'),
            preserve_default=True,
        ),
    ]
