# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name=b'\xd0\x91\xd1\x80\xd0\xb5\xd0\xbd\xd0\xb4')),
            ],
            options={
                'verbose_name': '\u0411\u0440\u0435\u043d\u0434\u044b',
                'verbose_name_plural': '\u0411\u0440\u0435\u043d\u0434',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CodeCpa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('shop', models.CharField(max_length=500, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('code', models.CharField(max_length=1000, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xb4 \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd\xd0\xb0')),
            ],
            options={
                'verbose_name': '\u041a\u043e\u0434\u044b \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u043e\u0432',
                'verbose_name_plural': '\u041a\u043e\u0434 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=250, null=True, verbose_name=b'Email_name', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd1\x84\xd0\xb8\xd0\xb9', blank=True)),
                ('urlback', models.URLField(max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82')),
                ('url', models.URLField(max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0')),
                ('public', models.IntegerField(default=0, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Items',
                'verbose_name_plural': 'Item',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'image', verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd1\x84\xd0\xb8\xd1\x8f', blank=True)),
                ('status', models.IntegerField(default=1, verbose_name=b'\xd0\xa1\xd1\x82\xd0\xb0\xd1\x82\xd1\x83\xd1\x81 \xd1\x84\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb3\xd1\x80\xd0\xb0\xd1\x84\xd0\xb8\xd0\xb8')),
                ('item', models.ForeignKey(related_name='items', to='item.Item')),
            ],
            options={
                'verbose_name': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u0438',
                'verbose_name_plural': '\u0424\u043e\u0442\u043e\u0433\u0440\u0430\u0444\u0438\u044f',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RelatedPhotos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('photo_additional', models.ForeignKey(related_name='photo_additional', to='item.Photo')),
                ('photo_general', models.ForeignKey(related_name='photo_general', to='item.Photo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SavedTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subs',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sub_to_user', models.ForeignKey(related_name='subs', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0', blank=True)),
                ('url_raw', models.URLField(default=b'', max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0 \xd0\xb1\xd0\xb5\xd0\xb7 \xd0\xba\xd0\xbe\xd0\xb4\xd0\xb0', blank=True)),
                ('x_position', models.CharField(max_length=250, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb7\xd0\xb8\xd1\x86\xd0\xb8\xd1\x8f X')),
                ('y_position', models.CharField(max_length=250, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb7\xd0\xb8\xd1\x86\xd0\xb8\xd1\x8f Y')),
                ('z_position', models.IntegerField(default=0, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xb7\xd0\xb8\xd1\x86\xd0\xb8\xd1\x8f Z')),
                ('brand_name', models.ForeignKey(related_name='tags', to='item.BrandName')),
                ('photo', models.ForeignKey(related_name='photos', to='item.Photo')),
            ],
            options={
                'verbose_name': '\u041c\u0435\u0442\u043a\u0438',
                'verbose_name_plural': '\u041c\u0435\u0442\u043a\u0430',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sex', models.IntegerField(default=0, verbose_name=b'\xd0\x9f\xd0\xbe\xd0\xbb')),
                ('image', models.ImageField(upload_to=b'image', null=True, verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xb7\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f', blank=True)),
                ('phone', models.CharField(max_length=250, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x82\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x84\xd0\xbe\xd0\xbd\xd0\xb0', blank=True)),
                ('link', models.URLField(max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0', blank=True)),
                ('description', models.CharField(max_length=150, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('pp', models.IntegerField(null=True, verbose_name=b'\xd0\xa6\xd0\xb5\xd0\xbd\xd0\xb0 product placement', blank=True)),
                ('email', models.CharField(max_length=250, verbose_name=b'Email \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xbe\xd1\x82\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xba\xd0\xb8 \xd0\xb4\xd0\xb0\xd0\xbd\xd0\xbd\xd1\x8b\xd1\x85', blank=True)),
                ('link_shop', models.URLField(max_length=1000, verbose_name=b'\xd0\xa1\xd1\x81\xd1\x8b\xd0\xbb\xd0\xba\xd0\xb0 \xd0\xbd\xd0\xb0 \xd0\xbc\xd0\xb0\xd0\xb3\xd0\xb0\xd0\xb7\xd0\xb8\xd0\xbd', blank=True)),
                ('bank_account_owner', models.CharField(max_length=500, verbose_name=b'\xd0\x92\xd0\xbb\xd0\xb0\xd0\xb4\xd0\xb5\xd0\xbb\xd0\xb5\xd1\x86 \xd0\xb1\xd0\xb0\xd0\xbd\xd0\xba\xd0\xbe\xd0\xb2\xd1\x81\xd0\xba\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xb0\xd0\xba\xd0\xba\xd0\xb0\xd1\x83\xd0\xbd\xd1\x82\xd0\xb0', blank=True)),
                ('bank_account_number', models.IntegerField(null=True, verbose_name=b'\xd0\x9d\xd0\xbe\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x81\xd1\x87\xd0\xb5\xd1\x82\xd0\xb0', blank=True)),
                ('country', models.CharField(max_length=150, verbose_name=b'\xd0\xa1\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb0', blank=True)),
                ('bank_code', models.IntegerField(null=True, verbose_name=b'\xd0\x9a\xd0\xbe\xd0\xb4 \xd0\xb1\xd0\xb0\xd0\xbd\xd0\xba\xd0\xb0', blank=True)),
                ('bank_name', models.CharField(max_length=250, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xb1\xd0\xb0\xd0\xbd\xd0\xba\xd0\xb0', blank=True)),
                ('wmr', models.IntegerField(null=True, verbose_name=b'Webmoney', blank=True)),
                ('yandex', models.IntegerField(null=True, verbose_name=b'\xd0\xaf\xd0\xbd\xd0\xb4\xd0\xb5\xd0\xba\xd1\x81 \xd0\x94\xd0\xb5\xd0\xbd\xd1\x8c\xd0\xb3\xd0\xb8', blank=True)),
                ('zip_code', models.CharField(max_length=250, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x87\xd1\x82\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9 \xd0\xb8\xd0\xbd\xd0\xb4\xd0\xb5\xd0\xba\xd1\x81', blank=True)),
                ('city', models.CharField(max_length=250, verbose_name=b'\xd0\x93\xd0\xbe\xd1\x80\xd0\xbe\xd0\xb4', blank=True)),
                ('address', models.CharField(max_length=500, verbose_name=b'\xd0\x90\xd0\xb4\xd1\x80\xd0\xb5\xd1\x81', blank=True)),
                ('status_pay', models.IntegerField(default=0, verbose_name=b'\xd0\xa1\xd0\xbf\xd0\xbe\xd1\x81\xd0\xbe\xd0\xb1 \xd0\xbe\xd0\xbf\xd0\xbb\xd0\xb0\xd1\x82\xd1\x8b')),
                ('user', models.ForeignKey(related_name='profile', to=settings.AUTH_USER_MODEL, unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='savedtag',
            name='tag',
            field=models.ForeignKey(related_name='tag', to='item.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='savedtag',
            name='user',
            field=models.ForeignKey(related_name='usertags', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
