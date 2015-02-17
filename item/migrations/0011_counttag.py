# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0010_getmoney'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_addr', models.CharField(default=0, max_length=250, verbose_name=b'IP')),
                ('http_user_agent', models.CharField(default=0, max_length=1000, verbose_name=b'Browser')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('tag', models.ForeignKey(related_name='tag_click', to='item.Tag')),
                ('user', models.ForeignKey(related_name='user_click', default=0, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
