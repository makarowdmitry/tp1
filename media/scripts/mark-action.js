// JavaScript Document

$(document).ready(function(){
	
	$(".mark-brand").click(function(){
            /*$(this).childern("#mark-close-use").attr('xlink:href','#close-mark');*/
            $(this).next('.brand-panel').toggle(0);
            
            

            function position() {
            $(this).siblings(".brand-panel").position({
                of: $( ".mark-brand-position1" ),
                my: "center center",
                at: "center bottom+6",
                collision: "flipfit",
                within: $( "#image" )
            });}

             
            position();
        }); 
});