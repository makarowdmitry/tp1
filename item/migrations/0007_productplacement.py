# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0006_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPlacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.IntegerField(default=0, max_length=9, verbose_name=b'price_product_placement', blank=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(related_name='pp_for_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
