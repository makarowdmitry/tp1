# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0018_auto_20150211_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productplacement',
            name='price',
            field=models.IntegerField(max_length=9, verbose_name=b'price_product_placement'),
            preserve_default=True,
        ),
    ]
