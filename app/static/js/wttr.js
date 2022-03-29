$(document).ready(function () {

	$.get("https://wttr.in/Berlin?format=3", function (data) {
		console.log(data)

		const words = data.split(' ');
		const wttr_icon = words[1];
		const wttr_text	= words[words.length - 1];

		$('#wettr_icon').text(wttr_icon);
		$('#wttr').text(wttr_text);
	});

});