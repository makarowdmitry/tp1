// JavaScript Document


$(document).ready(function(){

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
                         window.location.replace("/generation_links");
                        

                        }
                        

                    }
                });

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



});


