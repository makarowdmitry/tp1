// JavaScript Document

$(document).ready(function(){

/*Переключение radio*/
$('.bt-radio').toggle(
  
      function(){
      $(this).removeClass('checked');
      $(this).siblings('.bt-radio').addClass('checked');
      },
      function(){
      $(this).addClass('checked');
      $(this).siblings('.bt-radio').removeClass('checked');
      }
 
);



//Позиционирование элементов
setTimeout(function(){

$('.js-panel-brandname').each(function(){ 

            var tag_star_block = $(this).prev('.tag-star-block');
            var panel_brand = $(this);
            var tag_with_block = $(this).parents('.tag-with-block');


            function position() {
            panel_brand.position({
                of: tag_star_block,
                my: "center center",
                at: "center bottom+6",
                collision: "flipfit",
                within: tag_with_block
            });}

            position();
        });

},100);




/*СТРАНИЦА НАСТРОЕК*/

$('#js-women_check').click(function(){

    $(this).attr("class","bt-radio checked");//Включаем чекбокс
    $('#js-men_check').attr('class','bt-radio ');//Выключаем у другого поля
     $('[name="sexuser"]').val('women');//пишем значение в input
    
  });

  $('#js-men_check').click(function(){

    $(this).attr("class","bt-radio checked");//Включаем чекбокс
    $('#js-women_check').attr('class','bt-radio');//Выключаем у другого поля
    $('[name="sexuser"]').val('men');//пишем значение в input

  });

  //Отправка на сервер данных основные настройки
  $('.js-get-server-general-settings').click(function(){
    var username = $('[name="username"]').val();
    var raw_emailgeneral = $('[name="emailgeneral"]').val();
    var sexuser = $('[name="sexuser"]').val();
    var raw_description = $('[name="description"]').val();
    var raw_link = $('[name="link"]').val();
    var this_button = $(this);

    if(raw_description.length > 150 || ~raw_emailgeneral.indexOf('@')== false || ~raw_link.indexOf('http')== false){
          $('.js-error-text').hide(0);

          if(raw_description.length > 150){
            $('[name="description"]').prevAll('.js-error-text:first').fadeIn(300).text('Не более 150 символов'); 
      
          }
          

          if (~raw_emailgeneral.indexOf('@')== false){
           $('[name="emailgeneral"]').prevAll('.js-error-text:first').fadeIn(300).text('Email должен содержать @'); 
          }

          if (~raw_link.indexOf('http')== false){
            $('[name="link"]').prevAll('.js-error-text:first').fadeIn(300).text('Ссылка должна начинаться на http'); 
          }
    }

  
    else {
      var emailgeneral = $('[name="emailgeneral"]').val();
      var description = $('[name="description"]').val();
      var link = $('[name="link"]').val();


        $.ajax({
                    url: "/save_settings_general/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "username": username,
                        "email": emailgeneral,
                        "sex": sexuser,
                        "description": description,
                        "link": link


                                            },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {
                
                         $('.save-ok').show(0).delay(300);
                         $('.save-ok').hide(0);
                         $('.js-error-text').hide(0);
                      
                    }
        });
      

    }
  });


   //Отправка на сервер изменение пароля
  $('.js-get-server-password-settings').click(function(){
    var pass1 = $('[name="pass1"]').val();
    var pass2 = $('[name="pass2"]').val();
    var this_button = $(this);

    $.ajax({
                    url: "/save_settings_pass/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "pass1": pass1,
                        "pass2": pass2
                        

                                            },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {

                      if(data == 'ok') {
                       $('.save-ok').show(0).delay(300);
                       $('.save-ok').hide(0);
                       $('.js-error-text').hide(0);
                      }
                      else {
                        $(this_button).siblings('.js-error-text').fadeIn(300).text(data);           
                        
                      }
            }
        });

  });

  
 //Отправка на сервер данных бизнес настроек
  $('.js-get-server-business-settings').click(function(){
    var raw_email_for_data = $('[name="email"]').val();
    var pp = $('[name="pp"]').val();
    var raw_link_shop = $('[name="link_shop"]').val();
    var this_button = $(this);

    

    if((~raw_email_for_data.indexOf('@')== false && raw_email_for_data != '') || (~raw_link_shop.indexOf('http')== false && raw_link_shop != '')){
          $('.js-error-text').hide(0);

          if(~raw_email_for_data.indexOf('@')== false && raw_email_for_data != ''){
            $('[name="email"]').prevAll('.js-error-text:first').fadeIn(300).text('Email должен содержать @'); 
      
          }

          if (~raw_link_shop.indexOf('http')== false && raw_link_shop != ''){
            $('[name="link_shop"]').prevAll('.js-error-text:first').fadeIn(300).text('Ссылка должна начинаться на http'); 
          }
    }

  
    else {

      var email_for_data = $('[name="email"]').val();
      var link_shop = $('[name="link_shop"]').val();

        $.ajax({
                    url: "/save_settings_business/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "email_for_data": email_for_data,
                        "link_shop": link_shop,
                        "pp": pp
                                  },
                    error: function() {
                        
                    },

                    success: function(data) {
                
                         $('.save-ok').show(0).delay(300);
                         $('.save-ok').hide(0);
                         $('.js-error-text').hide(0);
                      
                    }
        });    

    }
});

//Показать-скрыть поля в зависимости от способа оплаты
$(document).on('change','select[name="withdrawal_type"]', function(){
  var withdrawal_type_test = $('select[name="withdrawal_type"] option:selected').val();
  if(~withdrawal_type_test.indexOf('bank')){
  $('[name="bank_account_owner"]').show(0);
  $('[name="bank_account_number"]').show(0);
  $('[name="bank_code"]').show(0);
  $('[name="bank_name"]').show(0);
  $(this).nextAll('label').show(0);

    $('input[name="yandex"]').hide(0);

    
    $('input[name="wmr"]').hide(0); 
    $('input[name="wmr"]').prev('p').hide(0);

  }
  else if(~withdrawal_type_test.indexOf('webmoney')){
    $(this).nextAll('input').hide(0);
    $(this).nextAll('label').hide(0);

    $('input[name="wmr"]').show(0);
    $(this).nextAll('p').show(0);
    
  }
    else if(~withdrawal_type_test.indexOf('yandex')){

    $(this).nextAll('input').hide(0);
    $(this).nextAll('label').hide(0);
    $(this).nextAll('p').hide(0);

    $('input[name="yandex"]').show(0);
    
  }
  
});



 //Отправка на сервер платежных данных
  $('.js-get-server-payment-settings').click(function(){
    var this_button = $(this);

    var country = $('select[name="country"] option:selected').val();
    var city = $('[name="city"]').val();
    var address= $('[name="address"]').val();
    var zip_code=$('[name="zip_code"]').val();
    var withdrawal_type=$('select[name="withdrawal_type"] option:selected').val();
    var bank_account_owner=$('[name="bank_account_owner"]').val();
    
   
    var bank_name=$('[name="bank_name"]').val();

    var bank_account_number=$('[name="bank_account_number"]').val();
    var bank_code=$('[name="bank_code"]').val();    
    var wmr=$('[name="wmr"]').val();
    var yandex=$('[name="yandex"]').val(); 

        $.ajax({
                    url: "/save_settings_payment/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "country": country,
                        "city": city,
                        "address": address,
                        "zip_code": zip_code,
                        "withdrawal_type": withdrawal_type,
                        "bank_account_owner": bank_account_owner,
                        "bank_account_number": bank_account_number,
                        "bank_code": bank_code,
                        "bank_name": bank_name,
                        "wmr": wmr,
                        "yandex": yandex
                        
                                  },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {
                
                         $('.save-ok').show(0).delay(300);
                         $('.save-ok').hide(0);
                         $('.js-error-text').hide(0);
                      
                    }
        }); 

  });


// Делаем select - страну, которая выбрана
var what_country = $('input[name=what-country]').val();

var choice_option = $('select[name=country] option[value='+what_country+']').attr("selected","selected");


/*СТРАНИЦА НАСТРОЕК END*/

// Появление и исчезновение основного меню
  $('.js-open-close-menu-general').toggle(
    function () {
        $('.js-menu-general').css("display","block");
      },
      function () {
        $('.js-menu-general').css("display","none");
      }
  );


  


  // Исчезновение дополнительного меню к каждому фото
  $(document).on('click', '.js-close-window-more', function(){

  $(this).parents('.window-menu-item-block').hide(0);
  $('.background-window').hide(0);
  //$(this).parents('.window-menu-item-block').children('.uptolike-buttons').remove();
  //$(this).parents('.window-menu-item-block').children('script').remove();
  return false;
 
  });


/*Подписывает на юзера*/
$("[class ^= js-subscribe-but]").click(function() {

 
      var user_to_sub = $(this).next("input:first").attr("value");
      var active_button =""+"";

      var raw_selector = "[class ^= js-subscribe-but-"+ user_to_sub +"]";
      var all_button_this_user = $(raw_selector);//Все кнопки с таким же class


                $.ajax({
                    url: "/subscribe/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "user_to_sub": user_to_sub
                                            },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {

                      var countsubs = $('.js-count-subs-this').text();
                      var new_countsubs_plus = parseInt(countsubs) + 1;
                      var new_countsubs_minus = parseInt(countsubs) - 1;

                       if (data == "sub"){

                        all_button_this_user.text('Отписаться').css("background","#6b6b6b");
                        $('.js-count-subs-this').text(new_countsubs_plus).css("color","#161616");

                       }
                       else{
                        all_button_this_user.text('Подписаться').css("background","#161616");
                          if (new_countsubs_minus < 1){
                            $('.js-count-subs-this').text(new_countsubs_minus).css("color","#fff");
                          }
                          else {
                            $('.js-count-subs-this').text(new_countsubs_minus).show(0).css("color","#161616");
                          }               
                       
                       }

                  
        
                    }
                });
            return false;
  });




//Окно со слайдами о телепорт

$(".button-open-slider").click(function(){
           $(".background-window").show(0);
           $("#slider-about").show(0);
           $(".slider-about-one").show(0);
           $(".slider-about-two").hide(0);
           $(".slider-about-three").hide(0);
           return false

        });

$(".button-open-slider-sub").click(function(){
           $(".email-submit").text('Подписаться').css("background-color","#2a26ea");
           $(".background-window").show(0);
           $("#slider-about").show(0);
           $(".slider-about-one").hide(0);
           $(".slider-about-two").hide(0);
           $(".slider-about-three").show(0);
           return false

        });

$(".slider-about-close").click(function(){
           $(".background-window").hide(0);
           $(".background-window2").hide(0);
           $("#slider-about").hide(0);
           return false

        });

$(".slider-about-one a").click(function(){
           $(".slider-about-one").hide(0);
           $(".slider-about-two").show(0);
           $(".slider-about-three").hide(0);
           return false

        });

$(".slider-about-two a").click(function(){
           $(".slider-about-one").hide(0);
           $(".slider-about-two").hide(0);
           $(".slider-about-three").show(0);
           return false

        });


//Окно со слайдами конец




$(".email-submit").click(function(){
  var sub_user_email = $('.email-sub-input').val();
  if (sub_user_email == ''){
	$('.email-check-window').css('color','red').text('Поле пустое, попробуйте еще');


  }
  else {

    $.ajax({
                    url: "/sub_user_email/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "sub_user_email": sub_user_email
                  
                    },
                    error: function() {
          
                    },

                    success: function(ok) {
                      
                        $('.email-check-window').css('color','green').text('Спасибо');
			$(".background-window").delay(1000).hide(0);
                        $("#slider-about").delay(1000).hide(0);
                      


                    }
                });

  }
});


//Загрузка контента дополнительного для главной страницы
$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    '/',
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page').data('start_item'));
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});

//Загрузка контента дополнительного для страницы username
$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_username').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
            var link_username_raw = $('#load_next_page_username').siblings('input').val();
            var link_username = '/'+link_username_raw;
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    link_username,
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page_username').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_username').data('start_item'));
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});



//Загрузка контента дополнительного для страницы item
$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_item').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
            var link_item_raw = $('#load_next_page_item').siblings('input').val();
            var link_item = '/'+link_item_raw;
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    link_item,
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page_item').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_item').data('start_item'));
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});



//Загрузка контента дополнительного для страницы subs
$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_subs').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
          
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    '/subscription',
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page_subs').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_subs').data('start_item'));
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});



//Загрузка контента дополнительного для страницы subs
$(function(){
    var App = {
        nextStartItem: 0,
        scrollThreshold: 100,
        loading: false,
        setStartItem: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_tag').data('start_item'));
            return app.nextStartItem;
        },
        LoadPage: function() {
            var app = this;
          
            if(!app.loading) {
                app.loading = true;
                app.nextStartItem = app.setStartItem();
                $.get(
                    '/saved_tag',
                    {
                        'start_from': app.nextStartItem,
                        'ajax': 'Y'
                    },
                    function (data) {
                        $('#place_for_next_page_tag').replaceWith($(data));
                        app.loading = false;
                    }
                )
            }
        },
        Init: function(){
            var app = this;
            app.nextStartItem = parseInt($('#load_next_page_tag').data('start_item'));
            $(window).scroll(function(){
                var documentHeight = $(document).height(),
                    windowHeight = $(window).height(),
                    scrollTop = $(window).scrollTop(),
                    n = documentHeight - windowHeight - scrollTop;
                if(n <= app.scrollThreshold) {
                    app.LoadPage();
                }
            })
        }
    };
    App.Init();
});


//Загрузка фото в настройках
$(function(){
    var $imageUpdateBlock = $('#image_update_block');
    $("#image_update_form").children('input').change(function () {
        $('#image_update_form').ajaxSubmit({
            beforeSubmit: function(){
                $imageUpdateBlock.addClass('load');
            },
            success: function(data){
                var $image = $imageUpdateBlock.find('img');
                if($image.size()==1){
                    $image.replaceWith($(data));
                } else {
                    $image.remove();
                    $imageUpdateBlock.prepend($(data));
                }
                $imageUpdateBlock.removeClass('load');
            }
        });
    });
});

//Функция добавления контента, нажатие кнопки в меню.
$(function(){
    $('#image_upload_form').children('input').change(function () {
        $('#image_upload_form').ajaxSubmit({
            beforeSubmit: function(){
            },

            success: function(data){

              if(~data['group'].indexOf('partner')){
               window.location.replace("/addpartner/" + data['item_id']);
              }
              else {
                window.location.replace("/add/" + data['item_id']);
              }

                var $item_id = data;
                
              }
        });
    });
});




$(document).on('click','.sets-item-block', function(){
  $(this).parents('.panel-block').prev('.photo-block').children('.photo-left-block').children('.tag-with-block:not(:first)').show(0);
  $(this).remove();
});


//Закрытие окна подсказки

$(document).on('click','.js-help-window-page-hide', function(){
  $(this).parent('.empty-content-block').hide(0);
  return false;

});


//Закрытие окна подсказки при "Больше не показывать"
$(document).on('click','.js-help-window-page-record', function(){
  var where_record =  $(this).next('input[type=hidden]').val();
  var this_elem = $(this)



  $.ajax({          
        url: "/help_update/",
        type: "POST",
        dataType:"html",
        data: {
        "where_record": where_record},
        error: function() {
        alert('Ошибка получения запроса');
        },
        success: function() {
       
          this_elem.parent('.empty-content-block').hide(0);
          return false;
        }});
});







});



//Лайки

$(document).on('click','.js-like-get', function(){

  var photo_this = $(this).parents('.panel-block').prev('.photo-block').children('.photo-left-block').children('.tag-with-block').children('[class ^= photo-for-tags]').attr('id');
  var this_like = $(this);

   $.ajax({          
        url: "/like/",
        type: "POST",
        dataType:"html",
        data: {
        "like_photo": photo_this},
        error: function() {
        alert('Ошибка получения запроса');
        },
        success: function(data) {
 

          if (data[0] > 0){
            this_like.siblings('p').text(data[0]);
          }
          else{
            this_like.siblings('p').text('');
          }

          if(data[1] == "n"){
            this_like.children('[class ^= favorite]').attr('class','favorite');
                   

          }
          else{
             this_like.children('[class ^= favorite]').attr('class','favorite yes-like');
              
            
          }


          return false;
        }}); 
});




$(document).scroll(function(){

$('.js-panel-brandname').each(function(){ 

            var tag_star_block = $(this).prev('.tag-star-block');
            var panel_brand = $(this);
            var tag_with_block = $(this).parents('.tag-with-block');


            function position() {
            panel_brand.position({
                of: tag_star_block,
                my: "center center",
                at: "center bottom+6",
                collision: "flipfit",
                within: tag_with_block
            });}

            position();



        }); 

});



//По нажатию на "Скопировать ссылку" - открывается поле
$(document).on('click','.js-link-copy', function(){
          $(this).hide();
           $(this).siblings(".js-block-input-copy").show(0);
           $(this).siblings(".js-block-input-copy").children(".js-input-link-copy").focus();
           $(this).siblings(".js-block-input-copy").children(".js-input-link-copy").select();
           return false

});


// Появление и исчезновение дополнительного меню к каждому фото
  $(document).on('click', '.js-open-close-window-more', function(){

  

  $('.background-window').show(0);
   $(this).parents('.panel-block').siblings('.window-menu-item-block').show(0);
 
  
 
  });

//Кнопка поделится
$(document).on('click','.js-share-get', function(){

 

  setTimeout(function(){

    //$('.window-menu-item-block-share').append('<div data-share-size="40" data-like-text-enable="false" data-background-alpha="0.0" data-pid="1338699" data-mode="share" data-background-color="#ffffff" data-share-shape="rectangle" data-share-counter-size="12" data-icon-color="#ffffff" data-text-color="#000000" data-buttons-color="#161616" data-counter-background-color="#ffffff" data-share-counter-type="disable" data-orientation="horizontal" data-following-enable="false" data-sn-ids="vk.ok.fb.tw.gp" data-selection-enable="false" data-exclude-show-more="true" data-share-style="0" data-counter-background-alpha="1.0" data-top-button="false" class="uptolike-buttons"></div>');

    (function(w,doc) {
                    if (!w.__utlWdgt) {
                    w.__utlWdgt = true;
                    var d = doc, s = d.createElement('script'), g = 'getElementsByTagName';
                    s.type = 'text/javascript'; s.charset='UTF-8'; s.async = true;
                    s.src = ('https:' == w.location.protocol ? 'https' : 'http')  + '://w.uptolike.com/widgets/v1/uptolike.js';
                    var h=d[g]('body')[0];
                    h.appendChild(s);
                    }})(window,document);

    
  },1);

  $('.background-window-share-window').show(0);
   $('.window-menu-item-block-share').show(0);


});


$(document).on('click','.background-window-share-window', function(){

   $('.window-menu-item-block-share').hide(0);
   $(this).hide(0);



});


//Открытие окна Условий использования

$(document).on('click','.goods-rules , .politic-rules', function(){

    var this_window = $('.windiw-info-block.processing');


   var what_button = $(this).attr('class');

   if(what_button =='goods-rules'){
  this_window.children('p:first').text('Условия предоставления услуг');
  this_window.children('.text-for-window.more-tr.processing').html('Текст просто текст. <br>Текст просто текст 2');
   }
    else{
  this_window.children('p:first').text('Политика конфиденциальности');
  this_window.children('.text-for-window.more-tr.processing').html('Текст просто текст3. <br>Текст просто текст 4'); }

  this_window.show(0);
   $('.background-window').show(0);


});


//Закрытие окна Условий использования
$(document).on('click','.button-general.bt-ok-rules', function(){

   $('.windiw-info-block.processing').hide(0);
   $('.background-window').hide(0);
   return false;
});


