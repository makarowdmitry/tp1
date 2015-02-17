# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Item(models.Model):
    name = models.CharField(max_length=250, verbose_name='Название фотографий', blank=True)
    urlback = models.URLField(max_length=1000, verbose_name='Ссылка на контент')
    user = models.ForeignKey(User)
    url = models.URLField(max_length=1000, verbose_name='Ссылка')
    public = models.IntegerField(verbose_name='Статус публикации', default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    

    def get_photos(self):
        return Photo.objects.filter(item=self)

    def get_photos_general(self):
        return Photo.objects.filter(item=self, status=1)


    def get_tags_with_url(self):
        photos = Photo.objects.filter(item=self)
        count_tags = 0

        for photo in photos:
            tags = Tag.objects.filter(photo=photo.id)
            for tag in tags:
                if 'http' in tag.url:
                    count_tags += 1

        return count_tags


    def get_photo_with_url(self):
        photos = Photo.objects.filter(item=self)
        count_photos = 0

        for photo in photos:
            tags = Tag.objects.filter(photo=photo.id)
            count_tags = 0
            for tag in tags:
                if 'http' in tag.url:
                    count_tags += 1
            if count_tags>0:
                count_photos += 1

        return count_photos

    def get_profile_user(self):
        return UserProfile.objects.filter(user=self.user.id)

    class Meta:
        verbose_name = 'Items'        
        verbose_name_plural = 'Item'

    def __unicode__(self):
        return u'%s %s %s' % (self.id, self.url, self.name)


class Photo(models.Model):
    image = models.ImageField(upload_to='image', verbose_name='Фотография', blank=True)
    item = models.ForeignKey(Item, related_name='items')
    status = models.IntegerField(verbose_name='Статус фотографии',default=1)

    def get_tags(self):
        return Tag.objects.filter(photo=self).order_by('-id')

    def get_related(self):
        try:
            select_photos = RelatedPhotos.objects.filter(photo_general_id=self)
        except:
            select_photos = 0
            return select_photos

        return select_photos

    def get_tags_with_link(self):
        return Tag.objects.filter(photo=self, url__startswith='http')

    def get_tags_with_link_additional(self):
        count_tags_all = 0
        select_photos = RelatedPhotos.objects.filter(photo_general_id=self)
        try:
            for select_photo in select_photos:
                photo = Photo.objects.get(id=select_photo.photo_additional_id)
                tags = Tag.objects.filter(photo=photo.id , url__startswith='http')
                count_tags_all += len(tags)
        except:
            count_tags_all+=0

        return count_tags_all


    def get_count_photo_with_link_additional(self):
        count_photo_all = 0
        select_photos = RelatedPhotos.objects.filter(photo_general_id=self)
        try:
            for select_photo in select_photos:
                photo = Photo.objects.get(id=select_photo.photo_additional_id)
                tags = Tag.objects.filter(photo=photo.id , url__startswith='http')
                count_tags_all = len(tags)
                if count_tags_all>0:
                    count_photo_all += 1

        except:
            count_photo_all+=0

        return count_photo_all


    def get_like_count(self):        
        count_like = len(Like.objects.filter(photo_id=self.id))
        return count_like

    def get_user_like_this_photo(self):
        list_user = Like.objects.filter(photo_id=self.id).values_list('user_id', flat=True)
        return list_user



    class Meta:
        verbose_name = 'Фотографии'
        verbose_name_plural = 'Фотография'

    def __unicode__(self):
        return u'%s %s' % (self.id, self.image)


class RelatedPhotos(models.Model):
    photo_general = models.ForeignKey(Photo, related_name='photo_general')
    photo_additional = models.ForeignKey(Photo, related_name='photo_additional')

    def get_photos(self):
        return Photo.objects.filter(id=self.photo_additional_id)



class BrandName(models.Model):
    name = models.CharField(max_length=250, verbose_name='Бренд')

    class Meta:
        verbose_name = 'Бренды'
        verbose_name_plural = 'Бренд'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    url = models.URLField(max_length=1000, verbose_name='Ссылка', blank=True)
    url_raw = models.URLField(max_length=1000, verbose_name='Ссылка без кода', blank=True, default='')
    brand_name = models.ForeignKey(BrandName, related_name='tags')
    x_position = models.CharField(max_length=250, verbose_name='Позиция X')
    y_position = models.CharField(max_length=250, verbose_name='Позиция Y')
    z_position = models.IntegerField(verbose_name='Позиция Z', default=0)
    photo = models.ForeignKey(Photo, related_name='photos')

    def get_brandname(self):
        return BrandName.objects.get(id=self.brand_name_id)

    def get_item(self):
        photo_this_tag = Photo.objects.get(id=self.photo_id)
        item_this_tag = Item.objects.get(id=photo_this_tag.item_id)
        return item_this_tag

    class Meta:
        verbose_name = 'Метки'
        verbose_name_plural = 'Метка'

    def __unicode__(self):
        return u'%s %s' % (self.url, self.brand_name)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    sex = models.IntegerField(verbose_name='Пол', default=0)
    image = models.ImageField(upload_to='image', verbose_name='Фото пользователя', blank=True, null=True)
    phone = models.CharField(max_length=250, verbose_name='Номер телефона', blank=True)
    link = models.URLField(max_length=1000, verbose_name='Ссылка', blank=True)
    description = models.CharField(max_length=150, verbose_name='Описание', blank=True)
    pp = models.IntegerField(verbose_name='Цена product placement', blank=True, null=True)
    email = models.CharField(max_length=250, verbose_name='Email для отправки данных', blank=True)
    link_shop = models.URLField(max_length=1000, verbose_name='Ссылка на магазин', blank=True)
    bank_account_owner = models.CharField(max_length=500, verbose_name='Владелец банковского аккаунта', blank=True)
    bank_account_number = models.IntegerField(verbose_name='Номер счета', blank=True, null=True)
    country = models.CharField(max_length=150, verbose_name='Страна', blank=True)
    bank_code = models.IntegerField(verbose_name='Код банка', blank=True, null=True)
    bank_name = models.CharField(max_length=250, verbose_name='Название банка', blank=True)
    wmr = models.IntegerField(verbose_name='Webmoney', blank=True, null=True)
    yandex = models.IntegerField(verbose_name='Яндекс Деньги', blank=True, null=True)
    zip_code = models.CharField(max_length=250, verbose_name='Почтовый индекс', blank=True)
    city = models.CharField(max_length=250, verbose_name='Город', blank=True)
    address = models.CharField(max_length=500, verbose_name='Адрес', blank=True)
    status_pay = models.IntegerField(verbose_name='Способ оплаты', default=0)
    price_cpa = models.DecimalField(verbose_name='Цена за клик по CPA модели', default=0.0, max_digits=10, decimal_places=4)

    help_subs = models.IntegerField(max_length=2, verbose_name="Подсказка на странице subscription", default=1)
    help_saved_tag = models.IntegerField(max_length=2, verbose_name="Подсказка на странице saved_tag", default=1)
    help_item = models.IntegerField(max_length=2, verbose_name="Подсказка на страницах item username index", default=1)
    help_sedit = models.IntegerField(max_length=2, verbose_name="Подсказка на странице sedit", default=1)
    help_analytics = models.IntegerField(max_length=2, verbose_name="Подсказка на странице analytics", default=1)
    help_add = models.IntegerField(max_length=2, verbose_name="Подсказка на странице addpartner", default=1)


    def __unicode__(self):
        return u'%s %s' % (self.user.username, self.sex)


class Subs(models.Model):
    user = models.ForeignKey(User, related_name='user')
    sub_to_user = models.ForeignKey(User, related_name='subs')

    def get_items(self):
        return Item.objects.filter(user=self.sub_to_user)


class SavedTag(models.Model):
    user = models.ForeignKey(User, related_name='usertags')
    tag = models.ForeignKey(Tag, related_name='tag')
    date = models.DateTimeField(auto_now_add=True, blank=True)
    item = models.ForeignKey(Item, related_name='item')

    """def get_items(self):
        return Item.objects.filter(id=self.item_id)"""


class Email(models.Model):
    email = models.CharField(max_length=250, verbose_name='Email_name', blank=True, null=True)

class CodeCpa(models.Model):
    shop = models.CharField(max_length=500, verbose_name='Название', blank=True)
    code = models.CharField(max_length=1000, verbose_name='Код магазина')

    class Meta:
        verbose_name = 'Коды магазинов'
        verbose_name_plural = 'Код магазина'

    def __unicode__(self):
        return u'%s %s' % (self.shop, self.code)


class Like(models.Model):
    user = models.ForeignKey(User, related_name='user_like')
    photo = models.ForeignKey(Photo, related_name='photo_like')

class ProductPlacement(models.Model):
    user = models.ForeignKey(User, related_name='pp_for_user')
    price = models.IntegerField(max_length=9, verbose_name='price_product_placement')
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return u'%s %s' % (self.price, self.user.username)

class GetMoney(models.Model):
    user = models.ForeignKey(User, related_name='get_money_this_user')
    money = models.IntegerField(max_length=10, verbose_name='money_for_user')
    date = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        date = str(self.date)
        money = str(self.money)+' rub'
        return u'%s %s %s' % (money, self.user.username, date)


class CountTag(models.Model):
    user = models.ForeignKey(User, related_name='user_click_tag',default=1)
    tag = models.ForeignKey(Tag, related_name='tag_click')
    remote_addr = models.CharField(max_length=250, verbose_name='IP',default=0)
    http_user_agent = models.CharField(max_length=1000, verbose_name='Browser',default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class CountItem(models.Model):
    user = models.ForeignKey(User, related_name='user_click_item',default=1)
    item = models.ForeignKey(Item, related_name='item_link_click')
    remote_addr = models.CharField(max_length=250, verbose_name='IP',default=0)
    http_user_agent = models.CharField(max_length=1000, verbose_name='Browser',default=0)
    referer = models.CharField(max_length=8388608,verbose_name='Referer',default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)

class CountUsername(models.Model):
    user = models.ForeignKey(User, related_name='user_who_clicks',default=1)
    user_page = models.ForeignKey(User, related_name='users_page_that_visited',default=1)
    remote_addr = models.CharField(max_length=250, verbose_name='IP',default=0)
    http_user_agent = models.CharField(max_length=1000, verbose_name='Browser',default=0)
    referer = models.CharField(max_length=8388608,verbose_name='Referer',default=0)
    date = models.DateTimeField(auto_now_add=True, blank=True)