# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse, HttpResponseRedirect
import random
from item.models import *
from .forms import *
import json
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Group
from django.conf import settings as st
from django.views.generic import UpdateView, DetailView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from allauth.account.models import EmailAddress
from operator import itemgetter
import datetime
from django.db.models import Count, Min, Sum
from django.db import connection
from django.core.mail import send_mail


def index(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    if "hi_teleport" in request.COOKIES:
        hi_teleport = str(1)
    else:
        hi_teleport=str(0)

    items_raw = Item.objects.filter(public=1)
    items_total = items_raw.count()
    start_from = int(request.GET.get('start_from', 0))
    is_ajax = request.GET.get('ajax', None) == 'Y'
    articles_per_page =  st.ARTICLES_PER_PAGE or 15
    next_start_from = start_from + articles_per_page
    items = items_raw.order_by('-id')[start_from:next_start_from]
    user = request.user
    if user.username:
        profile = UserProfile.objects.get(user_id=user.id)
    else:
        profile = 0

    subscription = Subs.objects.filter(user_id = user.id).values_list('sub_to_user_id', flat=True)


    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'



    form = AddPhoto
    response = render_to_response('articles.html',{'items':items, 'form':form, 'user':user, 'group':group, 'subscription':subscription, 'next_start_from': next_start_from, 'is_ajax': is_ajax, 'items_total': items_total, "hi_teleport": hi_teleport, 'profile': profile, })
    response.set_cookie("hi_teleport","hi-BJxFioebLl25JmJttk", max_age=8000000)
    return response


def send_lead(request):

    send_mail('Привет', 'Ну как дела у тебя?', 'noreply@teleport.ink',
    ['makarow.dmitry@gmail.com','dmitry.makarow@yandex.ru'], fail_silently=False)

    return HttpResponse()


def analytics(request):
    if not request.user.is_authenticated():
        return redirect('/')

    user = request.user
    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    partner_yes = 'partner' in groups_list
    profile = UserProfile.objects.get(user_id=user.id)

    #Если присутсвует "admin" присваем значение group = "admin"
    if partner_yes == 1:
        group = 'partner'
        try:
            get_money = GetMoney.objects.filter(user_id=user.id).order_by('-date')[0]
        except:
            get_money = '0'

        click_rate = round(profile.price_cpa,1)

        item_id_this_user = Item.objects.filter(user_id=user.id)
        count_item_raw = CountItem.objects.filter(item_id=item_id_this_user)
        count_item= count_item_raw.count()
        count_username = CountUsername.objects.filter(user_page_id=user.id).count()
        count_all_views = count_item+count_username





        count_subs = Subs.objects.filter(sub_to_user_id=user.id).count()

        list_item = []

        for item in item_id_this_user:
            item_id = item.id
            view_all = CountItem.objects.filter(item_id=item_id).count()
            view_vkcom = CountItem.objects.filter(item_id=item_id, referer__icontains='vk.com').count()
            view_facebook = CountItem.objects.filter(item_id=item_id, referer__icontains='facebook').count()
            view_instagram = CountItem.objects.filter(item_id=item_id, referer__icontains='instagram').count()
            view_youtube = CountItem.objects.filter(item_id=item_id, referer__icontains='youtube').count()
            view_odnoklassniki = CountItem.objects.filter(item_id=item_id, referer__icontains='odnoklas').count()
            view_other = view_all-view_vkcom-view_facebook-view_instagram-view_youtube-view_odnoklassniki

            photo_this_item = Photo.objects.filter(item_id=item_id)
            tags_this_photo = Tag.objects.filter(photo_id=photo_this_item)
            all_click_tag = CountTag.objects.filter(tag_id=tags_this_photo).count()

            income_all_this_item = int(all_click_tag*click_rate)

            item_data = {'id':item_id,'all':view_all,'vk':view_vkcom,'facebook':view_facebook,'instagram':view_instagram,'youtube':view_youtube,'odnoklass':view_odnoklassniki,'other':view_other,'all_click':all_click_tag,'income':income_all_this_item}
            list_item.append(item_data)




        #Данные для графика "Просмотры" c сделать список по минутам
        truncate_date = connection.ops.date_trunc_sql('minute','date')
        qs = count_item_raw.extra({'minute':truncate_date})
        now_date = datetime.datetime.now()




        list_all_minutes=[]
        i=0
        while i>-1500:#43200
            delta_time_this = datetime.timedelta(minutes=i)
            end_time = now_date+delta_time_this
            for_append = {'minute':end_time.replace(second=0,microsecond=0),'count':0}
            list_all_minutes.append(for_append)
            i=i-1



        result_list_raw  = qs.values('minute').annotate(count=Count('date'))
        q2  = qs.values('minute')

        result_list = []
        for res in result_list_raw:
            res_raw = res['minute']
            res_raw = res_raw.replace(tzinfo=None)
            result_list.append({'minute':res_raw,'count':res['count']})


        for item_l in list_all_minutes:
            for item_r in result_list:
                if item_l['minute'] == item_r['minute']:
                    item_l['count']=item_r['count']

        first_minute = list_all_minutes[0]['minute']

        for_chart_view = []
        for item_count in list_all_minutes:
            count_this = item_count['count']
            for_chart_view.append(count_this)

        for_chart_view.reverse()

        #Данные для графика "Клики" c сделать список по минутам



        photo_this_user = Photo.objects.filter(item_id=item_id_this_user)
        tags_this_user = Tag.objects.filter(photo_id=photo_this_user)
        count_click_tag = CountTag.objects.filter(tag_id=tags_this_user).count()

        income_cpa = int(click_rate*count_click_tag)
        income_pp_raw = ProductPlacement.objects.filter(user_id=user.id)

        income_pp = 0

        for income_pp_one in income_pp_raw:
            income_pp += income_pp_one.price

        income_all = income_pp + income_cpa


        return render_to_response('analytics.html',{'first_minute':first_minute, 'for_chart_view':for_chart_view,'q2':qs,'qs1':sorted(result_list_raw),'result_list':sorted(result_list),'list_all_minutes':list_all_minutes,'count_click_tag': count_click_tag , 'user':user, 'group':group, 'profile': profile, 'get_money':get_money, 'income_cpa':income_cpa, 'income_pp':income_pp, 'count_all_views':count_all_views, 'count_subs':count_subs,'click_rate':click_rate,'income_all':income_all, 'list_item':list_item})

def faq(request):
    if not request.user.is_authenticated():
        return redirect('/')

    user = request.user
    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    partner_yes = 'partner' in groups_list
    profile = UserProfile.objects.get(user_id=user.id)

    #Если присутсвует "admin" присваем значение group = "admin"
    if partner_yes == 1:
        group = 'partner'
    else:
        group = 0


    return render_to_response('faq.html',{'user':user, 'group':group, 'profile': profile})



def tag_redirect(request, tagid, itemid):
    tag = Tag.objects.get(id=tagid)
    url_for_redirect = tag.url

    #Записываем статистику по tag
    remote_addr = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']
    try:
        user_id=request.user.id
        save_tag = CountTag(user_id=user_id,tag_id=tagid,http_user_agent=user_agent,remote_addr=remote_addr)
        save_tag.save()
    except:
        save_tag = CountTag(tag_id=tagid,http_user_agent=user_agent,remote_addr=remote_addr)
        save_tag.save()


    #Записываем тег в ленту
    try:
        user = request.user
        tag_check = SavedTag.objects.filter(tag_id=tagid,user_id=user.id,item_id=itemid)
        if len(tag_check) == 0:
            tag = SavedTag(tag_id=tagid, user_id=user.id, item_id = itemid)
            tag.save()
    except:
        return redirect(url_for_redirect)



    return redirect(url_for_redirect)



def subscription(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    if "hi_teleport" in request.COOKIES:
        hi_teleport = str(1)
    else:
        hi_teleport=str(0)


    user = request.user
    subscription = Subs.objects.filter(user_id = user.id).values_list('sub_to_user_id', flat=True)
    all_item = Item.objects.filter(user_id=subscription).order_by('-date')


    items_total = all_item.count()
    start_from = int(request.GET.get('start_from', 0))
    is_ajax = request.GET.get('ajax', None) == 'Y'
    articles_per_page =  st.ARTICLES_PER_PAGE or 15
    next_start_from = start_from + articles_per_page
    items = all_item[start_from:next_start_from]

    if user.username:
        profile = UserProfile.objects.get(user_id=user.id)
    else:
        profile = 0




    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'



    form = AddPhoto
    response = render_to_response('subscription.html',{'all_item':all_item , 'form':form, 'user':user, 'group':group, 'subscription':subscription, 'next_start_from': next_start_from, 'is_ajax': is_ajax, "hi_teleport": hi_teleport, 'profile':profile,'items':items,'items_total':items_total})
    response.set_cookie("hi_teleport","hi-BJxFioebLl25JmJttk", max_age=8000000)
    return response



def save_tag(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        id_item_saved = request.POST.get("id_item_saved","")
        id_photo_saved = request.POST.get("id_photo_saved","")
        id_tag_saved = request.POST.get("id_tag_saved","")
        id_user = request.user.id

        save_tag_new, created = SavedTag.objects.update_or_create(tag_id=id_tag_saved, defaults={'photo_id': id_photo_saved, 'item_id': id_item_saved, 'user_id': id_user})

        return HttpResponse("ok")


    return HttpResponseBadRequest()



def saved_tag(request):
    if not request.user.is_authenticated():
        return redirect('/accounts/login/')

    user = request.user
    item_saved_this_user_raw_first = SavedTag.objects.filter(user_id=user.id).order_by('item_id').distinct('item_id')
    item_saved_this_user_raw_two = SavedTag.objects.filter(user_id=user.id).order_by('item_id')
    item_saved_this_user_raw = item_saved_this_user_raw_first.values('item_id', 'date')

    tag_saved_this_user = item_saved_this_user_raw_two.values_list('tag_id', flat=True)

    item_saved_this_user = sorted(item_saved_this_user_raw, key=itemgetter('date'), reverse=True)

    item_all = []

    for item_for_public in item_saved_this_user:
        item_once = Item.objects.get(id=item_for_public['item_id'])
        item_all.append(item_once)

    items_total = len(item_all)
    start_from = int(request.GET.get('start_from', 0))
    is_ajax = request.GET.get('ajax', None) == 'Y'
    articles_per_page =  st.ARTICLES_PER_PAGE or 15
    next_start_from = start_from + articles_per_page
    items = item_all[start_from:next_start_from]

    if user.username:
        profile = UserProfile.objects.get(user_id=user.id)
    else:
        profile = 0

    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'



    form = AddPhoto
    response = render_to_response('saved_tag.html',{'tag_saved_this_user':tag_saved_this_user, 'form':form, 'user':user, 'group':group, 'next_start_from': next_start_from, 'is_ajax': is_ajax, 'profile': profile,'items':items,'items_total': items_total})
    return response





def add_photo(request):
    if request.method == 'POST':
        images = request.FILES.getlist('image',[])
        item = Item(url='http://teleport.ink/', user=request.user)
        item.save()
        item.url += str(item.id)
        item.save()

        for_response_info = {}
        for_response_info['item_id'] = item.id

        group_list = request.user.groups.all().values_list('name', flat=True)
        if 'partner' in group_list:
            for_response_info['group'] = 'partner'

        else:
            for_response_info['group'] = 'none'



        for image in images:
            photo = Photo(image=image, item_id=item.id)
            photo.save()


    return HttpResponse(json.dumps(for_response_info), content_type="application/json")



def add_photo_more(request, id_item):
    if request.method == 'POST':
        images = request.FILES.getlist('image',[])
        for image in images:
            photo = Photo(image=image, item_id=id_item, status=1)
            photo.save()

    return redirect('/')



def add_additional_photo(request, id_item, id_photo):
    if request.method == 'POST':
        images = request.FILES.getlist('image',[])
        url_photo = []
        for image in images:
            photo = Photo(image=image, item_id=id_item, status=0)
            photo.save()
            related_photos = RelatedPhotos(photo_additional_id=photo.id ,photo_general_id=id_photo)
            related_photos.save()

            url_photo_this = {'id_image': str(photo.id), 'url_image': str(photo.image)}
            url_photo.append(url_photo_this)


    return HttpResponse(json.dumps(url_photo), content_type="application/json")
 

def add(request,item_id):
    user = request.user
    item = Item.objects.get(id=item_id)

    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list


    image_form = ProfileImageForm

    user_info = request.user
    profile = UserProfile.objects.get(user_id=user_info.id)

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'

    if group != 'moderator':
        if user.id != int(item.user_id):
            return redirect('/')




    #Выбрать всех пользователей принадлеж. к группе partner
    #all_partners = User.objects.user_groups.filter(group_id=1)
    all_partners =  User.objects.filter(groups=1)
    #all_partners = User.objects.all()

    if not request.user.is_authenticated():
        return redirect('/')

    form = ChangePhoto
    form1 = AddPhoto

    return render_to_response('add.html',{'form1':form1, 'form':form, 'profile':profile,'image_form': image_form,'item':item,"all_partners": all_partners, "group":group})


def addpartner(request,item_id):
    user = request.user
    item = Item.objects.get(id=item_id)

    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list


    image_form = ProfileImageForm

    user_info = request.user
    profile = UserProfile.objects.get(user_id=user_info.id)

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'

    if group != 'moderator':
        if user.id != int(item.user_id):
            return redirect('/')




    #Выбрать всех пользователей принадлеж. к группе partner
    #all_partners = User.objects.user_groups.filter(group_id=1)
    all_partners =  User.objects.raw('SELECT * FROM auth_user_groups WHERE group_id = %s', str(1))
    #all_partners = User.objects.all()

    if not request.user.is_authenticated():
        return redirect('/')

    form = ChangePhoto
    form1 = AddPhoto

    return render_to_response('addpartner.html',{'user':user, 'form1':form1, 'form':form, 'profile':profile,'image_form': image_form,'item':item,"all_partners": all_partners, "group":group})



def tag(request):
    if request.method == 'POST':
        x_position = request.POST.get('x_position')
        y_position = request.POST.get('y_position')
        photo = request.POST.get('photo')

        photo_this_tag = Photo.objects.get(id=int(photo))

        brandname = BrandName(name='')
        brandname.save()
        brand_name_id = brandname.id

        tag = Tag(brand_name_id=brand_name_id, x_position=x_position, y_position=y_position, photo_id=photo)
        tag.save()

        otvet = []
        photo_status = {'photo_status': str(photo_this_tag.status),'tagid': str(tag.id)}
        otvet.append(photo_status)

        return HttpResponse(json.dumps(otvet), content_type="application/json")


def tag_addpartner(request):
    if request.method == 'POST':
        x_position = request.POST.get('x_position')
        y_position = request.POST.get('y_position')
        photo = request.POST.get('photo')
        brandname_raw = request.POST.get('brandname')

        photo_this_tag = Photo.objects.get(id=int(photo))

        brandname = BrandName(name=brandname_raw)
        brandname.save()
        brand_name_id = brandname.id

        tag = Tag(brand_name_id=brand_name_id, x_position=x_position, y_position=y_position, photo_id=photo)
        tag.save()

        otvet = []
        photo_status = {'photo_status': str(photo_this_tag.status),'tagid': str(tag.id)}
        otvet.append(photo_status)

        return HttpResponse(json.dumps(otvet), content_type="application/json")





def tag_update(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name_date')
        url = request.POST.get('url')
        z_position = request.POST.get('z_position')
        tag_id = request.POST.get('tag_id')
        photo = request.POST.get('photo')

        brandname = BrandName(name=brand_name)
        brandname.save()
        brand_name_id = brandname.id

        tag = Tag.objects.get(id=tag_id)
        tag.url = url
        tag.brand_name_id = brand_name_id
        tag.z_position = z_position
        tag.save()

        tags_raw = Tag.objects.filter(photo_id=photo)
        tags = tags_raw.exclude(id=tag_id)

        if str(z_position) == '1':
            for tagin in tags:
                tagin.z_position = 0
                tagin.save()

        return HttpResponse(tag.id)


def tag_update_z_index(request):
    if request.method == 'POST':
        z_position = request.POST.get('z_position')
        tag_id = request.POST.get('tag_id')

        tag = Tag.objects.get(id=tag_id)
        tag.z_position = z_position
        tag.save()

        return HttpResponse()

def tag_update_url(request):
    if request.method == 'POST':
        url = request.POST.get('urlback')
        tag_id = request.POST.get('tag_id')
        urlgeneral = request.POST.get('urlgeneral')
        tag = Tag.objects.get(id=tag_id)
        tag.url_raw = url
        tag.save()
        photo = Photo.objects.get(id=tag.photo_id)
        item = Item.objects.get(id=photo.item_id)
        user = User.objects.get(id=item.user_id)
        username = user.username.upper()
        user_id = str(user.id)
        shops = CodeCpa.objects.all()
        for shop in shops:
            if shop.shop.lower() in url:
                code_shop = shop.code
                break

        try:
            tag.url = 'http://ad.admitad.com/goto/'+code_shop+'/?subid='+username+'_ID_'+user_id+'&ulp='+url
            tag.save()
        except:
            tag.url = urlgeneral
            tag.save()


        return HttpResponse(tag.url)


def tag_update_brand_name(request):
    if request.method == 'POST':
        brand_name = request.POST.get('brand_name_data')
        tag_id = request.POST.get('tag_id')

        brandname = BrandName(name=brand_name)
        brandname.save()
        brand_name_id = brandname.id

        tag = Tag.objects.get(id=tag_id)
        tag.brand_name_id = brand_name_id
        tag.save()

        return HttpResponse()

def tag_update_position(request):
    if request.method == 'POST':
        x_position = request.POST.get('x_position')
        y_position = request.POST.get('y_position')
        id_tag = request.POST.get('id_tag')

        tag = Tag.objects.get(id=id_tag)
        tag.x_position = x_position
        tag.y_position = y_position
        tag.save()

        return HttpResponse()

def delete_objects(request):
    if request.method == 'POST':
        what_delete = request.POST.get('name_delete')
        id_for_delete = request.POST.get('value_delete')

        if what_delete == 'tag':
            tag = Tag.objects.get(id=id_for_delete).delete()
            for_response = 'tag'+str(id_for_delete)

        elif what_delete == 'photo':
            photo = Photo.objects.get(id=id_for_delete)

            if photo.status == 1:
                photos_related = RelatedPhotos.objects.filter(photo_general_id=photo.id).delete()

            photo.delete()
            for_response = 'photo'+str(id_for_delete)


        elif what_delete == 'item':

            item = Item.objects.get(id=id_for_delete).delete()
            for_response = 'item'+str(id_for_delete)

        return HttpResponse(for_response)


def item_public_yes_no(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = Item.objects.get(id=item_id)


        groups_list = request.user.groups.all().values_list('name', flat=True)
        if 'partner' in groups_list:
            item.public = 1
            item.save()
        else:
            if item.public == 0:
                item.public = 1
                item.save()
            else:
                item.public = 0
                item.save()

        return HttpResponse(item.public)


def show_tag(request):
    if request.method == 'POST':
        photo_id = request.POST.get('photo_id')
        tags = Tag.objects.filter(photo_id=photo_id)

        data_all = []

        for tag in tags:
            tag_raw = {'tag_id':tag.id, 'x_position':tag.x_position, 'y_position':tag.y_position}
            data_all.append(tag_raw)

        return HttpResponse(json.dumps(data_all), content_type="application/json")

def delete_tag(request):
    if request.method == 'POST':
        tag_id = request.POST.get('tag_id')
        tag = Tag.objects.get(id=tag_id).delete()

        return HttpResponse(tag_id)



def item_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        tags_all = data['tags_all']
        photo = data['tags_all'][0]['photo']


        for tag in tags_all:
            x_position = tag['x_position']
            y_position = tag['y_position']
            tag_id = tag['id']
            item_id = tag['item_id']
            photo = tag['photo']
            name_item = tag['name_item']
            user_item = tag['user_item']
            item_url_back = tag['item_url_back']

            item = Item.objects.get(pk=item_id)
            if item.public == 0:
                item.public = 1
                item.save()
            item.name = name_item
            item.urlback = item_url_back
            user_item_this = User.objects.get(username=user_item)
            item.user_id = int(user_item_this.id)
            item.save()

            tag = Tag.objects.get(pk=tag_id)
            tag.x_position = x_position
            tag.y_position = y_position
            tag.save()

        tags = Tag.objects.filter(photo_id=photo)


        count_z = 0
        for tagin in tags:
            count_z += int(tagin.z_position)

        if count_z == 0:
            two_count = int(len(tags)-1)
            randomss = random.randint(0,two_count)
            tag_select = tags[randomss]
            tag_select_id = tag_select.id
            tag_z_index_change = Tag.objects.get(id=tag_select_id)
            tag_z_index_change.z_position = "1"
            tag_z_index_change.save()

        return HttpResponse("ok")


def get_tag(request):
    if request.method == 'POST':
        tag_id = request.POST.get('id')
        tag = Tag.objects.get(pk=tag_id)
        brand_name_id = tag.brand_name_id
        brand = BrandName.objects.get(pk=brand_name_id)


        response_data = {}
        response_data['brand_name'] = brand.name
        response_data['url'] = tag.url
        response_data['z_position'] = tag.z_position
        response_data['tag_id'] = tag.id

        return HttpResponse(json.dumps(response_data), content_type="application/json")


def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item_delete = Item.objects.filter(id=item_id).delete()
        return HttpResponse('delete')


def settings(request):
    if not request.user.is_authenticated():
        return redirect('/')

    #Берем список групп данного пользователя
    groups_list = request.user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'

    user_info = request.user
    profile = UserProfile.objects.get(user_id=user_info.id)
    image_form = ProfileImageForm
    return render_to_response('set.html',{'user':user_info, 'profile': profile, 'group':group, 'image_form': image_form})


def sedit(request):
    if not request.user.is_authenticated():
        return redirect('/')

    #Берем список групп данного пользователя
    groups_list = request.user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'


    user_info = request.user
    profile = UserProfile.objects.get(user_id=user_info.id)
    image_form = ProfileImageForm
    form = AddPhoto
    return render_to_response('seted.html',{'form':form,'user':user_info, 'profile': profile, 'group':group, 'image_form': image_form})


class PhotoUpdateView(UpdateView):
    model = UserProfile
    template_name = 'image_update.html'
    form_class = ProfileImageForm

    def get_success_url(self):
        return reverse('profile_image', args=[str(self.object.id)])

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PhotoUpdateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)
        form.instance.user = user
        form.instance.sex = user_profile.sex
        return super(PhotoUpdateView, self).form_valid(form)


class ProfileImageView(DetailView):
    model = UserProfile
    template_name = 'profile_image.html'
    context_object_name = 'profile'




def username(request, usernamethis):
    if "hi_teleport" in request.COOKIES:
        hi_teleport = str(1)
    else:
        hi_teleport=str(0)

    try:
        #Получаем данные юзера с ссылки
        username_raw = usernamethis
        user_this = User.objects.get(username__iexact=username_raw)
        id_user_this = int(user_this.id)
        profile_user_this = UserProfile.objects.get(user_id=id_user_this)
        items_user_this = Item.objects.filter(user_id=id_user_this,public=1).order_by('-date')
        user_this_count_subs_raw = Subs.objects.filter(sub_to_user_id=id_user_this)
        count_subs = len(user_this_count_subs_raw)

    except User.DoesNotExist:
        return redirect('/')

    try:
        referer=request.META['HTTP_REFERER']
    except:
        referer = 0


    remote_addr = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']

    try:
        count_username = CountUsername(user_id=request.user.id,user_page_id=id_user_this,remote_addr=remote_addr,http_user_agent=user_agent,referer=referer)
        count_username.save()
    except:
        count_username = CountUsername(user_page_id=id_user_this,remote_addr=remote_addr,http_user_agent=user_agent,referer=referer)
        count_username.save()

    items_raw = Item.objects.filter(public=1,user_id=id_user_this)
    items_total = items_user_this.count()
    start_from = int(request.GET.get('start_from', 0))
    is_ajax = request.GET.get('ajax', None) == 'Y'
    articles_per_page =  st.ARTICLES_PER_PAGE or 15
    next_start_from = start_from + articles_per_page
    items = items_user_this[start_from:next_start_from]
    user = request.user
    if user.username:
        profile = UserProfile.objects.get(user_id=user.id)
    else:
        profile = 0

    subscription = Subs.objects.filter(user_id = user.id).values_list('sub_to_user_id', flat=True)




    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list
    bigpartner_yes = 'bigpartner' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    if bigpartner_yes == 1:
        group = 'bigpartner'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'




    form = AddPhoto()
    response = render_to_response('articles_user.html',{'items':items,'count_subs': count_subs,'user_this':user_this,'id_user_this': id_user_this,'profile_user_this':profile_user_this,'items_user_this':items_user_this,'form':form, 'user':user, 'group':group, 'subscription':subscription, 'next_start_from': next_start_from, 'is_ajax': is_ajax, 'items_total': items_total, "hi_teleport": hi_teleport, 'profile': profile})
    response.set_cookie("hi_teleport","hi-BJxFioebLl25JmJttk", max_age=8000000)
    return response




def pageerror(request):
    return redirect('/')

def item(request, itemid):
    if "hi_teleport" in request.COOKIES:
        hi_teleport = str(1)
    else:
        hi_teleport=str(0)

    try:
        item_this_user = Item.objects.get(id=itemid)
        id_user_this = int(item_this_user.user_id)
    except:
        return redirect('/')

    try:
        referer=request.META['HTTP_REFERER']
    except:
        referer = 0


    remote_addr = request.META['REMOTE_ADDR']
    user_agent = request.META['HTTP_USER_AGENT']

    try:
        count_item = CountItem(user_id=request.user.id,item_id=itemid,remote_addr=remote_addr,http_user_agent=user_agent,referer=referer)
        count_item.save()
    except:
        count_item = CountItem(item_id=itemid,remote_addr=remote_addr,http_user_agent=user_agent,referer=referer)
        count_item.save()



    user_this = User.objects.get(id=id_user_this)
    profile_user_this = UserProfile.objects.get(user_id=id_user_this)
    items_user_this = Item.objects.filter(user_id=id_user_this).exclude(id=itemid).order_by('-date')
    user_this_count_subs_raw = Subs.objects.filter(sub_to_user_id=id_user_this)
    count_subs = len(user_this_count_subs_raw)
    user = request.user


    items_total = items_user_this.count()
    start_from = int(request.GET.get('start_from', 0))
    is_ajax = request.GET.get('ajax', None) == 'Y'
    articles_per_page =  st.ARTICLES_PER_PAGE or 15
    next_start_from = start_from + articles_per_page
    items = items_user_this[start_from:next_start_from]


    if user.username:
        profile = UserProfile.objects.get(user_id=user.id)
    else:
        profile = 0

    try:
        item_first_raw = int(itemid)
        item_first = Item.objects.get(id=item_first_raw)
    except:
        return redirect('/')





    subscription = Subs.objects.filter(user_id = user.id).values_list('sub_to_user_id', flat=True)


    #Берем список групп данного пользователя
    groups_list = user.groups.all().values_list('name', flat=True)
    parther_yes = 'partner' in groups_list
    moderator_yes = 'moderator' in groups_list
    admin_yes = 'admin' in groups_list
    user_yes = 'user' in groups_list

    #Если присутсвует "admin" присваем значение group = "admin"
    if admin_yes == 1:
        group = 'admin'
    #Если присутсвует "moderator" присваем значение group = "moderator"
    elif moderator_yes == 1:
        group = 'moderator'
    #Если присутсвует 'parther' присваем значение group = 'parther'
    elif parther_yes == 1:
        group = 'partner'
    #Иначе присваем значение group = "admin"
    else:
        group = 'user'

    form = AddPhoto()
    response = render_to_response('articles_item.html',{'items':items,'count_subs': count_subs,'user_this':user_this,'id_user_this': id_user_this,'profile_user_this':profile_user_this,'items_user_this':items_user_this,'form':form, 'user':user, 'group':group, 'subscription':subscription, 'item_first': item_first, "hi_teleport": hi_teleport, 'profile':profile,'next_start_from': next_start_from, 'is_ajax': is_ajax, 'items_total': items_total, })
    response.set_cookie("hi_teleport","hi-BJxFioebLl25JmJttk", max_age=8000000)
    return response



def login(request):
    if request.user.is_authenticated():
        return redirect('/')
    # args = {}
    # args.update(csrf(request))
    if request.POST:
        args = {}
        email = request.POST.get('email', '')
        username_raw = email.split("@")
        username_raw2 = username_raw[0]
        username = username_raw2.lower()
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html')


def logout(request):
    auth.logout(request)
    return redirect("/")


def register_new(request):
    if request.POST:
        args = {}
        email = request.POST.get('email', '').lower()
        password = request.POST.get('password', '')
        username_raw = email.split("@")
        username_raw2 = username_raw[0]
        username = username_raw2.lower()
        sex = request.POST.get('sex', '')
        group = Group.objects.get(name='user')



        user = User.objects.filter(email=email)
        if user:
            args['register_error'] = 'Такой пользователь уже есть!'
            return render_to_response('register.html', args)

        newuser = User.objects.create_user(username=username, password=password, email=email)
        newuser.save()

        user_id = newuser.id
        if sex == 'men':
            sex_value = 1
        else:
            sex_value = 0

        profile = UserProfile(user_id=user_id, sex = sex_value)
        profile.save()

        user_add_group = User.objects.get(id=user_id)

        user_add_group.groups.add(group)
        user_add_group.save()




        user_auth = auth.authenticate(username=username, password=password)
        auth.login(request, user_auth)
        return redirect('/')


def register(request):
    if request.user.is_authenticated():
        return redirect('/')
    return render_to_response('register.html')

def save_settings_general(request):
    if request.method == 'POST':
        username_raw = request.POST.get('username', '')
        username = username_raw.lower()
        email = request.POST.get('email', '')
        sex = request.POST.get('sex', '')
        link = request.POST.get('link', '')
        description = request.POST.get('description', '')

        if sex == 'men':
            sex_value = 1
        else:
            sex_value = 0

        user_info = request.user
        profile = UserProfile.objects.get(user_id=user_info.id)

        user = User.objects.get(username=request.user)
        user.email = email
        user.username = username

        email_address = EmailAddress.objects.get_primary(user)
        email_address.email = email
        email_address.save()

        user.save()
        profile.sex = sex_value
        profile.link = link
        profile.description = description
        profile.save()
        data = 'ok'


        return HttpResponse(data)


def save_settings_business(request):
    if request.method == 'POST':
        email_for_data = request.POST.get('email_for_data', '')
        link_shop = request.POST.get('link_shop', '')
        pp = request.POST.get('pp', '')

        user_info = request.user
        profile = UserProfile.objects.get(user_id=user_info.id)

        profile.pp = pp
        profile.link_shop = link_shop
        profile.email = email_for_data
        profile.save()

        data = 'ok'

        return HttpResponse(data)


def save_settings_payment(request):
    if request.method == 'POST':
        country = request.POST.get('country', '')
        city = request.POST.get('city', '')
        zip_code = request.POST.get('zip_code', '')
        bank_account_owner = request.POST.get('bank_account_owner', '')

        bank_name = request.POST.get('bank_name', '')

        raw_wmr = request.POST.get('wmr')
        raw_yandex = request.POST.get('yandex')
        raw_bank_account_number = request.POST.get('bank_account_number')
        raw_bank_code = request.POST.get('bank_code')

        address = request.POST.get('address', '')

        raw_withdrawal_type = request.POST.get('withdrawal_type')

        if raw_withdrawal_type == 'bank':
            status_pay = 0
        elif raw_withdrawal_type == 'webmoney':
            status_pay = 1
        else:
            status_pay = 2


        user_info = request.user
        profile = UserProfile.objects.get(user_id=user_info.id)

        profile.country = country
        profile.city = city
        profile.zip_code = zip_code
        profile.address = address
        profile.bank_account_owner = bank_account_owner
        profile.bank_name = bank_name

        if raw_wmr =='':
            profile.wmr = None
        else:
            profile.wmr = raw_wmr


        if raw_bank_account_number =='':
            profile.bank_account_number = None
        else:
            profile.bank_account_number = raw_bank_account_number


        if raw_bank_code =='':
            profile.bank_code = None
        else:
            profile.bank_code = raw_bank_code


        if raw_yandex =='':
            profile.yandex = None
        else:
            profile.yandex = raw_yandex


        profile.status_pay = status_pay
        profile.save()

        data = 'ok'

        return HttpResponse(data)


def save_settings_pass(request):
    if request.method == 'POST':
        pass1 = request.POST.get('pass1', '')
        pass2 = request.POST.get('pass2', '')

        user = User.objects.get(username=request.user)


        if pass1 != pass2:
            data = 'Пароли должены совпадать'

        elif len(pass1) < 6 or len(pass2) < 6:
            data = 'Длина пароля минимум 6 символов'

        else:
            user.set_password(pass2)
            user.save()
            user_auth = auth.authenticate(username=request.user, password=pass1)
            auth.login(request, user_auth)
            data = 'ok'


        return HttpResponse(data)


def subscribe(request):
    if not request.user.is_authenticated():
        return redirect('/')
    if request.POST:
        user_to_sub = request.POST.get('user_to_sub')
        user_id = request.user.id



        subs_check = Subs.objects.filter(sub_to_user_id=user_to_sub, user_id=user_id)

        user_this_count_subs_raw = Subs.objects.filter(sub_to_user_id=user_to_sub)
        data_new = {}
        data_new['csubs'] = str(len(user_this_count_subs_raw))



        if subs_check:
            subs_check.delete()
            data = 'unsub'
        else:
            subs = Subs(sub_to_user_id = user_to_sub, user_id = user_id)
            subs.save()
            data = 'sub'



        return HttpResponse(data)



def sub_user_email(request):
    if request.method == 'POST':
        sub_user_email = request.POST.get('sub_user_email', '')
        new_email = Email(email=sub_user_email)
        new_email.save()
        data = 'Спасибо'

        return HttpResponse(data)


def save_general_settings_item(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        urlback = request.POST.get('urlback', '')
        item_id = request.POST.get('id', '')
        item_user = request.POST.get('user_item', '')

        if item_user != '':
            user = User.objects.get(username=item_user)
        else:
            user = User.objects.get(username=request.user)


        item = Item.objects.get(id=int(item_id))
        item.name = name
        item.urlback = urlback
        item.user_id = user.id
        item.save()

        data = 'ok'

        return HttpResponse(data)

def partner_signup(request):
    return render_to_response('singuppartner.html')


def change_photo(request):
    if request.method == 'POST':
        image = request.FILES['image']
        photo = Photo.objects.get(id=request.POST['id_photo'])
        photo.image = image
        photo.save()
        photo_new = str(photo.image)

    return HttpResponse(photo_new)

def generation_links(request):
    if not request.user.is_authenticated():
        return redirect('/')

    #Берем список групп данного пользователя
    groups_list = request.user.groups.all().values_list('name', flat=True)
    moderator_yes = 'moderator' in groups_list

    if moderator_yes==1:
        try:
            tag = Tag.objects.filter(url='').order_by('id').exclude(brand_name__name ='').first()
            tag_photo_id = tag.photo_id
            photo = Photo.objects.get(id = tag_photo_id)
            tags_count = len(Tag.objects.filter(url='').exclude(brand_name__name =''))-1
            return render_to_response('page_for_generation_links.html',{'tag':tag, 'photo':photo, 'tags_count':tags_count})
        except:
            return redirect('/')

    else:
        return redirect('/')



def help_update(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        where_record = request.POST.get('where_record')
        profile = UserProfile.objects.get(user_id=request.user.id)


        if where_record=='saved_tag':

            profile.help_saved_tag = 0
            profile.save()

        elif where_record=='subscription':

            profile.help_subs = 0
            profile.save()

        return HttpResponse()


def like(request):
    if not request.user.is_authenticated():
        return redirect('/')

    if request.method == 'POST':
        like_photo = request.POST.get('like_photo')
        check_like = Like.objects.filter(user_id=request.user.id, photo_id=like_photo)

        if len(check_like) == 0:
            like = Like(user_id=request.user.id, photo_id=like_photo)
            like.save()
            like_status = 'yes'
        else:
            check_like.delete()
            like_status = 'no'

        count_like = len(Like.objects.filter(photo_id=like_photo))

        #for_response = {'count': count_like ,'status': like_status}
        for_response = [count_like,like_status]


        #return HttpResponse(json.dumps(for_response), content_type="application/json")
        return HttpResponse(for_response)







