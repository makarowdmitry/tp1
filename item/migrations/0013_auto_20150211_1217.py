# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0012_auto_20150210_1727'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('remote_addr', models.CharField(default=0, max_length=250, verbose_name=b'IP')),
                ('http_user_agent', models.CharField(default=0, max_length=1000, verbose_name=b'Browser')),
                ('referer', models.CharField(default=0, max_length=8388608, verbose_name=b'Referer')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('item', models.ForeignKey(related_name='item_link_click', to='item.Item')),
                ('user', models.ForeignKey(related_name='user_click_item', default=1, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='counttag',
            name='user',
            field=models.ForeignKey(related_name='user_click_tag', default=1, to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
