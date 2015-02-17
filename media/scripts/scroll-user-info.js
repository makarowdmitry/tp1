// JavaScript Document
/*$(document).ready(function(){        
        //Scroll user-info
        var h_hght = 41; // высота шапки
        var h_mrg = -10;     // отступ когда шапка уже не видна
        $(function(){
            $(window).scroll(function(){
                var top = $(this).scrollTop();
                var elem = $('.user-info-general');
                if (top+h_mrg < h_hght) {
                    elem.css({top:h_hght-top});
                    
                } else {
                elem.css('top', h_mrg);
                }
            });
        });

        
        
        

    }); 