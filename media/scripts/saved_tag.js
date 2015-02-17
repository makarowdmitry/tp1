// JavaScript Document
$(document).ready(function(){
    $("[class ^= saved-tag-]").click(function() {

      var id_item_saved = $(this).children(".saved-id-item").attr("value");
      var id_photo_saved = $(this).children(".saved-id-photo").attr("value");
      var id_tag_saved = $(this).children(".saved-id-tag").attr("value");

                $.ajax({
                    url: "/save_tag/",
                    type: "POST",
                    dataType:"html",
                    data: {
                        "id_item_saved": id_item_saved,
                        "id_photo_saved": id_photo_saved,
                        "id_tag_saved": id_tag_saved
                                            },
                    error: function() {
                        alert('Ошибка получения запроса');
                    },

                    success: function(data) {
                        
                    }
                }); 
            
	});

});