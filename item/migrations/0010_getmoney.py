# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0009_auto_20150210_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='GetMoney',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('money', models.IntegerField(default=0, max_length=10, verbose_name=b'money_for_user')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='get_money_this_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
