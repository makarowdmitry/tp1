// JavaScript Document


$(document).ready(function(){
//Создание метки по клику на фотографию
    $("#image").click(function(e) {        
        var offset = $(this).offset(); 
        
        x_position = (e.pageX - offset.left);
        y_position = (e.pageY - offset.top);
        photo_id = $(this).siblings("#photo_id").attr("value");
        

            /*function random_class_mark() {
                var class_mark = [
                'star-green-active',
                'star-yellow-active',
                'star-red-active',
                'star-blue-active',
                'star-fiolet-active'
                ];
                var number = Math.round(Math.random() * (class_mark.length-1));
                // Возвращаем строку:
                return class_mark[number];
            }

        var markColor = random_class_mark();*/
        $(this).parents('#photo-block').append('<div class="mark-brand" id=""><svg class="star-mark" viewBox="0 0 105 105"><use xlink:href="#star-mark"></use></svg></div>');
        $(this).siblings(".mark-brand:last").css({"margin":"0px", "top":y_position-15,"left":x_position-15, "z-index": 999});
        tag_id = $(this).siblings(".mark-brand:last");
        $(this).siblings(".mark-brand").draggable({ containment:'#image'});     
        $("#window-additional").show(0);
        $("#background-window").show(0);

        
    });

//Передвижение меток
    $(".mark-brand").draggable({ containment:'#image'});        

//Cоздание новой метки
    $("#tag_add").click(function() {
        var brand_name = $("input[name=brand_name]");
        var url = $("input[name=url]");
        var error = "";
        var url_date = url.val();
        var brand_name_date = brand_name.val();
        var z_position = 1;

        // Проверка на наличие названия бренда
        if (brand_name.val() == '') {
             error = "Укажить название бренда";
             alert(error);
        }

        // Если бренд указали. Создаем метку
        else{
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
                        alert(ok);
                    }
                });
            }

            $("#window-additional").hide(0);
            $("#background-window").hide(0);
        }
        
        return false;
});


//Публикация item
$("#post").click(function() {       
    var tags = $(".mark-brand");
    tags_all = {"tags_all":[]};
    tag_end = [];

    $.each(tags, function(i, val) {
       var id = $(this).attr("id");
       var y_position = $(this).css("top");
       var x_position = $(this).css("left");
       
       var tag = {
        "id": id,
        "x_position": x_position,
        "y_position": y_position
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

//По нажатию на метку item скрываем окно
$('#back-create').click(function(){
    $(".mark-brand:last").remove();
    $("#window-additional").hide(0);
    $("#background-window").hide(0);
});


//По нажатию на метку
$('.mark-brand').click(function(){
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
            
            brand_name2 = data.brand_name;
            tag_url = data.url;
            z_position2 = data.z_position;
            

            $('#brand_name').attr('value', brand_name2);
            $('#tag_url').attr('value', tag_url);
            $("#window-additional").show(0); //Показываем форму со значениями.
            $("#background-window").show(0); 
        }
    });


    
});

//Удаление item
$("#delete-photo-yes").click(function(){

    var item_id = $("article").attr("id");

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
            document.location.replace('/');
        }
    });


});

});
