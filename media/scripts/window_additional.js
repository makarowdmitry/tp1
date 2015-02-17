// JavaScript Document

$(document).ready(function(){
	
	$("#button-add-edit").click(function(){
           $("#background-window").fadeIn(0);
           $("#window-additional").slideDown(0);

        });

	$("#close-window-additional").click(function(){
           $("#background-window").fadeOut(0);
           $("#window-additional").slideUp(0);

        });

	$("#delete-mark-photo").click(function(){
           $(".window-section-one").hide(0);
           $(".window-section-two").show(0);

        });
	$("#сancel-window-additional").click(function(){
           $("#background-window").hide(0);
           $("#window-additional").hide(0);

        });

	$("#yes-delete-window-additional").click(function(){
     $(".window-section-two").hide(0);
     $(".window-section-one").show(0);
     $("#background-window").hide(0);
     $("#window-additional").hide(0);


       $(".section-success").show(0);
       $(".section-success").text("Удалено");
      setTimeout(function() { 
       $(".section-success").fadeOut(100);          
        }, 2000);

    });

    $("#link-copy-success").click(function(){
	   $("#background-window").hide(0);
       $("#window-additional").hide(0);
       $(".section-success").show(0);
       $(".section-success").text("Ссылка скопирована");
    	setTimeout(function() { 
       $(".section-success").fadeOut(100);          
        }, 2000);

    });

    



	


	
});