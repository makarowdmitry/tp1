# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='savedtag',
            name='item',
            field=models.ForeignKey(related_name='item', default=558, to='item.Item'),
            preserve_default=True,
        ),
    ]
