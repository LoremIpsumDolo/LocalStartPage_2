$(document).ready(function () {
	$(".button").click(function () {
		$(this).parent().parent().find(".input").toggle("slow");
		$(this).parent().parent().find(".label_value").toggle("slow");
		$(this).parent().find(".button").toggle("slow");
	});

	// $(".button_cancel").click(function () {
	// 	$(".input:visible").toggle("slow");
	// 	$(this).parent().find(".button").toggle("slow");
	// });

});