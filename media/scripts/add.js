// JavaScript Document


$(document).ready(function(){

$(function(){
    $('#image_upload_form').children('input').change(function () {
        setTimeout(function(){location.reload();}, 300);
        
    });
});


// Сохранение основных настроек для item(name, urlback)
$('.change_info_item1, .change_info_item2, .change_info_item3').change(function(){
    var name_item = $('[name = name_item]').val();
    var urlback_item = $('[name = urlback_item]').val();
    var id_item = $('[name = id_item]').val();
    var user_item = $("select#js-username_select").val();

    var this_button = $(this);


    $.ajax({ //Делаем запрос на сервер и получаем ответ в виде json
        url: "/save_general_settings_item/",
        type: "POST",
        dataType:"html",
        data: {
                "id": id_item,
                "name" : name_item,
                "urlback" : urlback_item,
                "user_item" : user_item,
        },
        error: function() {
            alert('Ошибка получения запроса');
        },

        success: function(data) {
            
            $('.save-ok').show(0).delay(300);
            $('.save-ok').hide(0);

        }
    });
    


});



//По нажатию на метку
$('.js-mark-brand').click(function(){
    var tag_id = $(this).attr("id");//Берем ее id
     $.ajax({ //Делаем запрос на сервер и получаем ответ в виде json
        url: "/get_tag/",
        type: "POST",
        dataType:"json",
        data: {
                "id": tag_id,
        },
        error: function() {
            alert('Ошибка получения запроса');
        },

        success: function(data) {
            
            var brand_name2 = data.brand_name;
            var tag_url = data.url;
            var z_position2 = data.z_position;
            var tag_id2 = data.tag_id;
            
            if(z_position2 == '1'){
                $("#check-yes2").attr("class","checkbox checkbox-two checkbox-two-checked");
            }
            else{
                $("#check-yes2").attr("class","checkbox checkbox-two");
            }

            $('.window-section-three #brand_name').attr('value', brand_name2);
            $('.window-section-three #tag_url').attr('value', tag_url);
            $('.window-section-three .tag_id2').attr('value', tag_id2);
            $('.window-section-four .tag_id3').attr('value', tag_id2);
            $("#window-additional").show(0); //Показываем форму со значениями.
            $(".window-section-one").hide(0);
            $(".window-section-two").hide(0);
            $(".window-section-four").hide(0);
            $(".window-section-three").show(0);
            $("#background-window").show(0); 
        }
    });


    
});


$(document).on('click', '.tag-with-block', function (ev) {
   
    // Генерация цвета для метки
    // Берем все метки на данной фотографии. Cчитаем их количество.
    $count_tag_this_photo = String($(this).children('.tag-star-block').length+1);


    var div = $('<div class="tag-star-block js-mark-brand"><p>'+$count_tag_this_photo+'</p><svg class="tag-star" viewBox="0 0 24 24"><use xlink:href="#star-mark-count"></use></svg></div>');
    var panel_with_tag = $(this).parents('.photo-left-block').parents('.photo-block').next('.panel-block').next('.tag-block-edit-general');
    
    //Добавление панели для меток
    
    $(this).children('.block-help-click').remove();//Удаление окна (Кликните по фотографии, чтобы добавить метку)


    $(this).prepend(div);

    //Позиционирование созданной метки
    div.position({
        my: "center center",
        of: ev,
        collision: "none",
        within: ".tag-with-block"
  
    });
    //Курсор при перетаскивании
    $(div).css('cursor','move');

    pos = div.position(),
        h = $(this).height(),
        w = $(this).width(),
        x_position = String(Math.round(pos.left * 100 / w))+ "%",
        y_position = String(Math.round(pos.top * 100 / h)) + "%";
        mark_h = String(27 * 100/h);
        mark_w = String(27 * 100/w);        
        x_position_test = parseInt(x_position);
        y_position_test = parseInt(y_position);

    if (x_position_test < 0){
        x_position = '0'+'%';
    }
    else if (x_position_test > (100-mark_w)){
        x_position = String(100-mark_w)+'%';
    }


    if (y_position_test < 0){
        y_position = '0'+'%';
    }
    else if (y_position_test > (100-mark_h)){
        y_position = String(100-mark_h)+'%';
    }



    div.css({
        "left":x_position,
        "top":y_position       
    });
    div.tooltip({ content:x_position+y_position});

    $photo_id_raw = $(this).children("img").attr("id");
    $photo_id_raw2 = $photo_id_raw.replace('img','');
    photo_id = parseInt($photo_id_raw2);


    div.draggable(

        {
            containment: "parent",
            stop: function (){
             var l = ( 100 * parseFloat($(this).css("left")) / parseFloat($(this).parent().css("width")) )+ "%" ;
             var t = ( 100 * parseFloat($(this).css("top")) / parseFloat($(this).parent().css("height")) )+ "%" ;
             $(this).css("left" , l);
             $(this).css("top" , t);
             var id_tag = $(this).attr('id');

             $.ajax({
                    url: "/tag_update_position/",
                    type: "POST",
                    dataType:"json",
                    data: {
                        "x_position": l,
                        "y_position": t,
                        "id_tag": id_tag
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    }

                    
                });
             

             }
        }
    );


    $.ajax({
                    url: "/tag/",
                    type: "POST",
                    dataType:"json",
                    data: {
                        "x_position": x_position,
                        "y_position": y_position,
                        "photo": photo_id
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {


                        if (data[0]['photo_status']==1){
                            $(panel_with_tag).prepend('<div class="tag-block-edit tag'+data[0]['tagid']+'"><div class="tag-block-edit-left"><a href="" class="tag-star-block" target="_blank" ><p>'+$count_tag_this_photo+'</p><svg class="tag-star" viewBox="0 0 24 24"><use xlink:href="#star-mark-count"></use></svg></a></div><div class="tag-block-edit-right"><input type="hidden" name="tag_id" value="'+data[0]['tagid']+'"/><label>Название бренда</label><input type="text" value="" name="brand_name" /><label>Ссылка</label><input type="text" value="" name="url_tag"/><div class="bt-radio-block"><div class="bt-check">Product placement</div></div><div class="menu-item-block delete-bt-color tag-block-edit-right-delete js-button-delete"><svg class="menu-item-block-svg" viewBox="0 0 24 24"><use xlink:href="#delete" ></use></svg></div><input type="hidden" name="what_delete" value="'+data[0]['tagid']+'tag" /></div></div>');

                        }
                        else {
                            $(panel_with_tag).prepend('<div class="tag-block-edit tag'+data[0]['tagid']+'"><div class="tag-block-edit-left"><a href="" class="tag-star-block" target="_blank" ><p>'+$count_tag_this_photo+'</p><svg class="tag-star" viewBox="0 0 24 24"><use xlink:href="#star-mark-count"></use></svg></a></div><div class="tag-block-edit-right"><input type="hidden" name="tag_id" value="'+data[0]['tagid']+'"/><label>Ссылка</label><input type="text" value="" name="url_tag"/><div class="menu-item-block delete-bt-color tag-block-edit-right-delete js-button-delete"><svg class="menu-item-block-svg" viewBox="0 0 24 24"><use xlink:href="#delete" ></use></svg></div><input type="hidden" name="what_delete" value="'+data[0]['tagid']+'tag" /></div></div>');
                        }       
                        
                        $(div).addClass('tag'+data[0]['tagid']);
                        $(div).attr('id', data[0]['tagid']);
                    }
                });

});


$(document).on('click','.js-button-delete', function (e){
    var status_delete = $(this);
    var $what_delete = $(this).siblings('[name=what_delete]').val();   
    $id_this_object = parseInt($what_delete);

    if(~$what_delete.indexOf('tag')){
        $('.windiw-info-block').children('.text-for-window').text('Удалить Метку навсегда?');
        $info_this_object = 'tag';

    }
    else if(~$what_delete.indexOf('photo')){
        $('.windiw-info-block').children('.text-for-window').text('Удалить Фото навсегда?');
        $info_this_object = 'photo';
    }
    else if(~$what_delete.indexOf('item')){
        $('.windiw-info-block').children('.text-for-window').text('Удалить все фотографии навсегда?');
        $info_this_object = 'item';
        
    }

    $('.windiw-info-block').children('.what-do').attr('name',$info_this_object).val($id_this_object);
    $('.background-window').show(0);
    $('.windiw-info-block').show(0);    

});

//Закрыть окно
$('.button-additional.bt-no, .button-general.bt-ok').click(function(){
    $('.background-window').hide(0);
    $('.windiw-info-block').hide(0);
});

//Удаление объекта
$(document).on('click','.button-general.bt-yes', function(){
    var name_delete_for_request = $(this).next('.what-do').attr('name');
    var value_delete_for_request = $(this).next('.what-do').val();

     $.ajax({
                    url: "/delete_objects/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "value_delete": value_delete_for_request,
                        "name_delete": name_delete_for_request
                        
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(ok) {
                        if(~ok.indexOf('item')){
                            window.location.replace("/");
                        }
                        else{
                        $('.background-window').hide(0);
                        $('.windiw-info-block').hide(0);
                        var select_element_for_delete = '.'+ok;
                        $(select_element_for_delete).remove();
                
                        $('.save-ok').show(0).delay(300);
                        $('.save-ok').hide(0);
                        

                        }
                        

                    }
                });

});

//Сохранение при включение Product Placement
$(document).on('click', '.bt-check', function (e) {

  var checked_yes_no = $(this).attr('class');
  var tag_id_for_check = $(this).parent('.bt-radio-block').siblings('[name = tag_id]').val();

  if(~checked_yes_no.indexOf('checked'))
  {
    $(this).removeClass('checked');
    var z_position_this_tag = 0;


  }
  else {
    $(this).addClass('checked');
    var z_position_this_tag = 1;
  }

  $.ajax({
                    url: "/tag_update_z_index/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "z_position": z_position_this_tag,
                        "tag_id": tag_id_for_check
                      
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function() {
                        $('.save-ok').show(0).delay(300);
                        $('.save-ok').hide(0);
                    }

                    
    });

});


//Декодируем ссылки при генерации страницы

$('[name=url_tag]').each(function(i, el){

    var $this_value_all = $(this).val();
    var end_value_url =  decodeURIComponent($this_value_all);
    $(this).val(end_value_url);
    

});

//Сохранение Обновление ccылки тега
$(document).on('change', '[name=url_tag]', function (e) {
  var this_tag = $(this);
  var tag_id_for_check = $(this).siblings('[name = tag_id]').val();
  var tad_url_update = $(this).val();

   if ( /^https?:/.test(tad_url_update)){

    $.ajax({
                    url: "/tag_update_url/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "urlback": encodeURIComponent(tad_url_update),
                        "tag_id": tag_id_for_check,
                        "urlgeneral":tad_url_update
                      
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {
                        $('.save-ok').show(0).delay(300);
                        $('.save-ok').hide(0);
                        var url_update_tag = this_tag.parent('.tag-block-edit-right').prev('.tag-block-edit-left').children('a').attr('href', String(data));
                        this_tag.prev('label').text('Ссылка').removeClass('error-label');
                        this_tag.removeClass('error-input');
                    }                    
    });

   }
   else {
    this_tag.prev('label').text('Ссылка должна начинаться с http:// либо https://').addClass('error-label');
    this_tag.addClass('error-input');
   }
});

//Обновление BrandName
$(document).on('change', '[name=brand_name]', function (e) {
  var this_tag = $(this);
  var tag_id_for_check = $(this).siblings('[name = tag_id]').val();
  var brand_name_update = $(this).val();

  $.ajax({
                    url: "/tag_update_brand_name/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "brand_name_data": brand_name_update,
                        "tag_id": tag_id_for_check
                      
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function() {
                        $('.save-ok').show(0).delay(300);
                        $('.save-ok').hide(0);
                    
    
                    }                    
    });

});


      
//Cоздание новой метки
    $("#tag_add").click(function() {
        var brand_name = $("input[name=brand_name]");
        var url = $("input[name=url]");
        var error = "";
        var url_date_raw = url.val();

        if ( /^https?:/.test(url_date_raw) && url_date_raw != "") {
            var url_date = url_date_raw;
        
        
        var brand_name_date = brand_name.val();
        var z_position_raw = $("#check-yes").attr("class");

        if(z_position_raw == "checkbox checkbox-two checkbox-two-checked"){
            var z_position = 1;
        }
        else{
            var z_position = 0;
        }

        
        // Если бренд указали. Создаем метку
        
            if (!error) {    
                $.ajax({
                    url: "/tag/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "brand_name_date": brand_name_date,
                        "url": url_date,
                        "x_position": x_position,
                        "y_position": y_position,
                        "z_position": z_position,
                        "photo": photo_id
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(ok) {
                        tag_id.attr("id", ok);
                        tag_id.attr("class", "mark-brand");
                        $("#check-yes").attr("class","checkbox checkbox-two");
                        $("#window-additional").hide(0);
                        $("#background-window").hide(0);
                    }
                });
            }
            
        
        
        return false;

        }
        else{
            alert("Ссылка обязательна и должна начинаться с http: или https: !");
        }
});


//Обновление метки
    $("#tag_update").click(function() {
        var brand_name = $(".window-section-three input[name=brand_name]");
        var url = $(".window-section-three input[name=url]");
        
        var url_date_raw = url.val();

        if ( /^https?:/.test(url_date_raw) && url_date_raw != "") {
            var url_date = url_date_raw;
        
        var brand_name_date = brand_name.val();
        var photo_id7 = $(".photo_id").attr("value");

        var z_position_raw = $("#check-yes2").attr("class");

        if(z_position_raw == "checkbox checkbox-two checkbox-two-checked"){
            var z_position2 = 1;
        }
        else{
            var z_position2 = 0;
        }

      

        var tag_id3 = $(".window-section-three .tag_id2").attr("value");
         
            $.ajax({
                    url: "/tag_update/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "brand_name_date": brand_name_date,
                        "url": url_date,
                        "z_position": z_position2,
                        "tag_id": tag_id3,
                        "photo": photo_id7
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    }

                    
                });
            

            $("#window-additional").hide(0);
            $("#background-window").hide(0);
        
        
        return false;
    }

        else{
            alert("Ссылка обязательна и должна начинаться с http: или https: !");
        }
});




//Публикация item
$("#post").click(function() {       
    var tags = $(".js-mark-brand");
    tags_all = {"tags_all":[]};
    tag_end = [];

    $.each(tags, function(i, val) {
       var id = $(this).attr("id");
       // Найти % и все числа перед ним
       
       var tag_position = $(this).attr("style");
       var myRe = /(\d*\.*\d*%)/g;
       var position_all = [];

        while ((myArray = myRe.exec(tag_position)) != null) {
            position_all += myArray[0]+',';
        }
        var the_end_position = position_all.split(',');

       var y_position = the_end_position[0];
       var x_position = the_end_position[1];

       
       var name_item = $('#item_name').val();
       var user_item = $("select#js-username_select").val();
       var item_url_back = $('#item_url_back').val();
       var item_id = $("article").attr("id");
       var photo_id8 = $(".photo_id").attr("value");
       var z_position = $(this).siblings("#tag_z_position").attr("value");
     


       var tag = {
        "id": id,
        "x_position": x_position,
        "y_position": y_position,
        "item_id": item_id,
        "photo": photo_id8,
        "name_item": name_item,
        "user_item": user_item,
        "item_url_back": item_url_back,
        }

    

       tag_end[i] = tag;

     });

    tags_all["tags_all"] = tag_end;
    data_tag = JSON.stringify(tags_all);
   

    // Отправка данных на сервер
    $.ajax({
        url: "/item_post/",
        type: "POST",
        dataType:"html",
        data: data_tag,
        error: function() {
            alert('Ошибка получения запроса');
        },

        success: function(ok) {
            var id = $('article').attr('id');
            document.location.replace('/#'+id);
        }
    });

});

//Присваиваем статус public
$(document).on('click','.js-public-yes-no', function(){
    var this_button = $(this);
    var item_id = $('article').attr('id');
    $.ajax({
                    url: "/item_public_yes_no/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "item_id": item_id
                      
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {
                        if (data==1){
                            this_button.text('Cнять с публикации').addClass('bt-no-public');
                        }   
                        else if(data==0){
                            this_button.text('Опубликовать').removeClass('bt-no-public');
                        }             
    
                    }                    

    });


});



//Удаление item
$(".yes-delete").click(function(){
        var item_id = $("article").attr("id");
        var item_id_prev = item_id-1;
        // Отправка данных на сервер
        $.ajax({
            url: "/delete_item/",
            type: "POST",
            dataType:"html",
            data: {
                 "item_id": item_id,
            },
            error: function() {
                alert('Ошибка получения запроса');
            },

            success: function(ok) {
                document.location.replace('/#'+item_id_prev);
            }
        });
    });


//Удаление tag
$(".yes-delete-mark").click(function(){
        var tag_id4 = $(this).siblings(".tag_id3").attr("value");
        // Отправка данных на сервер
        $.ajax({
            url: "/delete_tag/",
            type: "POST",
            dataType:"html",
            data: {
                 "tag_id": tag_id4,
            },
            error: function() {
                alert('Ошибка получения запроса');
            },

            success: function(data) {
                var data_tag = '#'+data;
                $(data_tag).remove();
                $("#window-additional").hide(0); //Показываем форму со значениями.
                $("#background-window").hide(0); 
            }
        });
    });


//Закрытие страницы при отмене
$(".cancel-page").click(function(){

    var item_id = $("article").attr("id");
    document.location.replace('/#'+item_id);

});

$(".js-mark-brand").css('cursor','move');

//Передвижение меток
$(".js-mark-brand").draggable(

{
    containment: "parent",
    stop: function (){
     var l = ( 100 * parseFloat($(this).css("left")) / parseFloat($(this).parent().css("width")) )+ "%" ;
     var t = ( 100 * parseFloat($(this).css("top")) / parseFloat($(this).parent().css("height")) )+ "%" ;
     $(this).css("left" , l);
     $(this).css("top" , t);
     var id_tag = $(this).attr('id');

             $.ajax({
                    url: "/tag_update_position/",
                    type: "POST",
                    dataType:"json",
                    data: {
                        "x_position": l,
                        "y_position": t,
                        "id_tag": id_tag
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    }

                    
                });


     }

}
    );  


//Изменение фотографий основных



$(document).on('change', '.change-photo-content input',
function () {
        $input_this_form = $(this);
        $(this).parents('.change-photo-content').ajaxSubmit({
            beforeSubmit: function(){
             
            },
             error: function() {
                alert('Ошибка получения запроса');
            },
            success: function(data){
               
                //Выбрать фотку под панелью
                $id_photo_this =  $input_this_form.siblings('input').val();
                $for_change_src = '#img'+ $id_photo_this;
                $link_for_image = '/uploads/'+data;
                $for_change_src_go = $($for_change_src).attr("src", $link_for_image);
              
                
              
            }
        });
    });

//Добавление фотографий образов
$(function(){
    $(".add-additional-photo-content").children('input').change(function () {
        $input_this_form = $(this);
        $(this).parents('.add-additional-photo-content').ajaxSubmit({
            beforeSubmit: function(){
            
            },
            error: function() {
                alert('Ошибка получения запроса');
            },

            success: function(data){
                
                
                $id_photo_this2 =  $input_this_form.siblings('input').val();
                $for_search_id_img = '#img'+ $id_photo_this2;
                $for_after_add_content = $($for_search_id_img).parents('.tag-with-block').parents('.photo-left-block').parents('.photo-block').next('.panel-block').next('.tag-block-edit-general');
                
               
                for (var i = data.length - 1; i >= 0; i--) {
                    
                    $div_content = $('<div class="photo-block photo'+data[i]['id_image']+'"><div class="photo-left-block"><div class="tag-with-block moderator-page"><img id="img'+data[i]['id_image']+'" src="/uploads/'+data[i]['url_image']+'"></div></div></div><div class="panel-block photo'+data[i]['id_image']+'"><div class="menu-item-block delete-bt-color js-button-delete"><svg class="menu-item-block-svg" viewBox="0 0 24 24"><use xlink:href="#delete" ></use></svg></div><input type="hidden" name="what_delete" value="'+data[i]['id_image']+'photo" /><div class="photo-item-block"><p class="text-on-button">изменить фото</p><svg class="photo-item-block-svg" viewBox="0 0 24 24"><use xlink:href="#change-photo" ></use></svg><form class="change-photo-content" enctype="multipart/form-data" method="post" action="/change_photo/"><input id="id_image" name="image" type="file" /><input type="hidden" value="'+data[i]['id_image']+'" name="id_photo" /></form></div></div><div class="tag-block-edit-general photo'+data[i]['id_image']+'"></div>');
                    $for_after_add_content.append($div_content);
                    
                };  
              
            }
        });
    });
});







});


