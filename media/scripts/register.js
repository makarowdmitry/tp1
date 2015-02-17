// JavaScript Document
$(document).ready(function(){
	$('#women_check').click(function(){

		$(this).attr("class","checkbox radio-one radio-one-checked");//Включаем чекбокс
		$('#men_check').attr('class','checkbox radio-one');//Выключаем у другого поля
		$('#sex_value').attr('value','women');//пишем значение в input
		
	});

	$('#men_check').click(function(){

		$(this).attr("class","checkbox radio-one radio-one-checked");//Включаем чекбокс
		$('#women_check').attr('class','checkbox radio-one');//Выключаем у другого поля
		$('#sex_value').attr('value','men');//пишем значение в input

	});
});