// JavaScript Document

$(document).ready(function(){

//Функция добавления фотографии
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
    var user_item = '';

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


//СОЗДАНИЕ НОВОЙ МЕТКИ





$(document).on('click','.js-button-delete', function (e){
    var status_delete = $(this);
    var $what_delete = $(this).siblings('[name=what_delete]').val();   
    $id_this_object = parseInt($what_delete);

    if(~$what_delete.indexOf('tag')){
        $('.windiw-info-block.delete-window').children('.text-for-window').text('Удалить Метку навсегда?');
        $info_this_object = 'tag';

    }
    else if(~$what_delete.indexOf('photo')){
        $('.windiw-info-block.delete-window').children('.text-for-window').text('Удалить Фото навсегда?');
        $info_this_object = 'photo';
    }
    else if(~$what_delete.indexOf('item')){
        $('.windiw-info-block.delete-window').children('.text-for-window').text('Удалить все фотографии навсегда?');
        $info_this_object = 'item';
        
    }

    $('.windiw-info-block.delete-window').children('.what-do').attr('name',$info_this_object).val($id_this_object);
    $('.background-window').show(0);
    $('.windiw-info-block.delete-window').show(0);    

});



//Закрыть окно
$('.delete-window .button-additional.bt-no, .button-general.bt-ok, .bt-no-change-mark').click(function(){
    $('.background-window').hide(0);
    $('.windiw-info-block.delete-window').hide(0);
    $('.windiw-info-block.processing').hide(0);
    $('.windiw-info-block.change-brandname').hide(0);

});


//Закрыть окно и удалить метку
function delete_tag(){
$(function(){
    $('.background-window').hide(0);
    $('.windiw-info-block.add-brandname').hide(0);
    var value_tag_id = $('.windiw-info-block.add-brandname [type=hidden]').val();
    $('.tag-with-block').children('.tag'+value_tag_id).remove();
    $('.windiw-info-block.add-brandname').children('[type="hidden"]').removeClass('tag'+value_tag_id);

     $.ajax({
                    url: "/delete_objects/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "value_delete": value_tag_id,
                        "name_delete": 'tag'
                        
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(ok) {

                    }
                });

});

};

$('.button-additional.bt-no-mark').click(function(){
    delete_tag();
});








//Удаление объекта
$(document).on('click','.button-general.delete-yes', function(){
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
                        $('.windiw-info-block.delete-window').hide(0);
                        var select_element_for_delete = '.'+ok;
                        $(select_element_for_delete).remove();
                
                        $('.save-ok').show(0).delay(300);
                        $('.save-ok').hide(0);
                        

                        }
                        

                    }
                });

});





//Показываем-скрываем окно для настроек видео
$(document).on('click', '.bt-check', function (e) {

  var checked_yes_no = $(this).attr('class');


  if(~checked_yes_no.indexOf('checked'))
  {
    $(this).removeClass('checked');
    $(this).next('.settings-input').hide(0);


  }
  else {
    $(this).addClass('checked');
   $(this).next('.settings-input').show(0);
  }

});




//Сохранение BrandName
$(document).on('click', '.windiw-info-block .bt-yes-save', function (e) {
  var tag_id_for_check = $(this).siblings('[type = "hidden"]').val();
  var brand_name_update = $(this).siblings('[type = "text"]').val();


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
                        $('.background-window').hide(0);
                        $('.windiw-info-block.add-brandname, .windiw-info-block.change-brandname').hide(0);
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
                    $('.background-window').show(0); 
                    $('.windiw-info-block.processing').show(0);
                    }                    

    });


});

//Удаление tag
$(".yes-delete-mark").click(function(){
        var tag_id4 = $(this).siblings('input[type="hidden"]').val();
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
                $('.background-window').hide(0); 
                $('.windiw-info-block.change-brandname').hide(0);
            }
        });
    });


//Изменяем курсор
$(".js-mark-brand").css('cursor','pointer');

//Передвижение меток
$(".js-mark-brand").draggable(

{
    containment: "parent",
    start: function(){
        $(this).css('cursor','move');
    },
    stop: function (){
        $(this).css('cursor','pointer');
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

});  


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

});





$(document).on('click', '.tag-with-block', function (ev) {
  
    var div = $('<div class="tag-star-block js-mark-brand"><svg class="tag-star" viewBox="0 0 24 24"><use xlink:href="#star-mark"></use></svg></div>');
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
    $(div).css('cursor','pointer');

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

    $('.windiw-info-block.add-brandname').children('[type="text"]').val('');
    $('.background-window').show(0);
    $('.windiw-info-block.add-brandname').show(0);


    div.draggable(
        {
            containment: "parent",
            start: function(){
                 $(this).css('cursor','move');
            },

            stop: function (){ 
            $(this).css('cursor','pointer');        

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
                    },
                    success: function(){

                    }
            });
            }}
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
                        
                        $(div).addClass('tag'+data[0]['tagid']);
                        $(div).attr('id', data[0]['tagid']);
                        
                        $('.windiw-info-block.add-brandname').children('[type="hidden"]').val(data[0]['tagid']).removeClass().addClass('tag'+data[0]['tagid']);
                            


                    }
                });

        });


//Клик по уже существующей метке
$(document).on('click','.js-mark-brand', function(){
    $(this).parent('.tag-with-block').off("click");



   var tag_id = $(this).attr('id');


    $.ajax({
        url:'/get_tag/',
        type:'POST',
        dataType:'json',
        data: {
            'id': tag_id
        },
        error: function(){alert('Ошибка запроса');},
        success: function(data){
        $('.windiw-info-block.change-brandname').children('input[type="text"]').val(data['brand_name']);
        $('.windiw-info-block.change-brandname').children('[type="hidden"]').val(tag_id);
        $('.windiw-info-block.change-brandname').show(0);
        $('.background-window').show(0);


        }
    });

return false;





});