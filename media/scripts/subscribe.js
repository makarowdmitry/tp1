// JavaScript Document
$(document).ready(function(){
    $("[class ^= subscribe-but]").click(function() {



  
    	var user_to_sub = $(this).next("input").attr("value");
    	var active_button =""+"";

    	var raw_selector = "[class ^= subscribe-but-"+ user_to_sub +"]";
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

                      var countsubs = $('.count-subs-this').text();
                      var new_countsubs_plus = parseInt(countsubs) + 1;
                      var new_countsubs_minus = parseInt(countsubs) - 1;

                       if (data == "sub"){

                        all_button_this_user.text('Отписаться').css("background","#6b6b6b");
                        $('.count-subs-this').text(new_countsubs_plus).show(0).css("background","#6b6b6b");

                       }
                       else{
                        all_button_this_user.text('Подписаться').css("background","#161616");
                          if (new_countsubs_minus < 1){
                            $('.count-subs-this').text(new_countsubs_minus).hide(0);
                          }
                          else {
                            $('.count-subs-this').text(new_countsubs_minus).show(0).css("background","#161616");
                          }               
                       
                       }

                  
        
                    }
                });
            return false
	});

});