# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0007_productplacement'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='price_cpa',
            field=models.IntegerField(default=0, max_length=12, verbose_name=b'\xd0\xa1\xd0\xbf\xd0\xbe\xd1\x81\xd0\xbe\xd0\xb1 \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd1\x8b'),
            preserve_default=True,
        ),
    ]
