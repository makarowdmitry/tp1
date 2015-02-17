// JavaScript Document
$(document).ready(function(){
	$("#image").click(function(e) {
		var offset = $(this).offset();
		var relativeX = (e.pageX - offset.left);
		var relativeY = (e.pageY - offset.top);

		function random_class_mark() {
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

		var markColor = random_class_mark();



	  $(this).parents('#photo-block').append('<div class="mark-brand"><svg class="star-mark '+markColor+'" viewBox="0 0 105 105"><use xlink:href="#star-mark"></use></svg></div>');
	  $(this).siblings(".mark-brand:last").css({"margin":"0px", "top":relativeY-15,"left":relativeX-15, "z-index": 999});
	  $(this).siblings(".mark-brand:last").draggable({ containment:'#image, .mark-brand'});	
	 
	  $("#window-additional").show(0);
	  $("#background-window").show(0);
	});




		//По клику: создаем метку в месте клика. сохраняем ее координаты в перменную. открываем окно.
		//По нажатию в окне на создать: Формируем JSON объект(из названия бренда, ссылки если есть, позиция X, позиции Y, позиция Z) и передаем данные по адресу методом POST

		//Получаем данные в форме JSON от сервера и добавляем метки и изменения.
		
		//При изменение значения кординат формируем Json и отправляем на сервер.

// Отправляем данные по AJAX
	
	});

	
