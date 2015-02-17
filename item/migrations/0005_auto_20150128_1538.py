# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0004_help'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='help',
            name='user',
        ),
        migrations.DeleteModel(
            name='Help',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_add',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5 addpartner'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_analytics',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5 analytics'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_item',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0\xd1\x85 item username index'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_saved_tag',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5 saved_tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_sedit',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5 sedit'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='help_subs',
            field=models.IntegerField(default=1, max_length=2, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb4\xd1\x81\xd0\xba\xd0\xb0\xd0\xb7\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb5 subscription'),
            preserve_default=True,
        ),
    ]
