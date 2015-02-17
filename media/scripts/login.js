// JavaScript Document
$(document).ready(function(){

//Проверка логина
    $("#login_check").click(function() {
    	var username = $("form input[name=username]").val();
        var password = $("form input[name=password]").val();

         
            $.ajax({
                    url: "/auth/login/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "username": username,
                        "password": password
                    },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },
                    success: function(data) {
                    	var data_check = data;
                        if(data_check == "ok"){
                        	alert("ok");

                        }
                        else(data_check == "no"){
                        	alert("no");
                        }
                    }

                    
                });
        
        
        return false;
});


});
