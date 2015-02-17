# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0002_savedtag_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savedtag',
            name='item',
            field=models.ForeignKey(related_name='item', to='item.Item'),
            preserve_default=True,
        ),
    ]
