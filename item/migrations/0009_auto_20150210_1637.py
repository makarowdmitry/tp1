# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_userprofile_price_cpa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='price_cpa',
            field=models.DecimalField(default=0.0, verbose_name=b'\xd0\xa6\xd0\xb5\xd0\xbd\xd0\xb0 \xd0\xb7\xd0\xb0 \xd0\xba\xd0\xbb\xd0\xb8\xd0\xba \xd0\xbf\xd0\xbe CPA \xd0\xbc\xd0\xbe\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb8', max_digits=10, decimal_places=4),
            preserve_default=True,
        ),
    ]
