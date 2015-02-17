# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0013_auto_20150211_1217'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountUsername',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_addr', models.CharField(default=0, max_length=250, verbose_name=b'IP')),
                ('http_user_agent', models.CharField(default=0, max_length=1000, verbose_name=b'Browser')),
                ('referer', models.CharField(default=0, max_length=8388608, verbose_name=b'Referer')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='user_who_clicks', default=1, to=settings.AUTH_USER_MODEL)),
                ('user_page', models.ForeignKey(related_name='users_page_that_visited', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
