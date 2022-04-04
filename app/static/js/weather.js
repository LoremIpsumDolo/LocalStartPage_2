$(document).ready(function () {
    // yes I know, this sucks and i will fix it...maybe

    var modal = document.getElementById("WeatherModal");
    var btn = document.getElementById("weather_module");

    btn.onclick = function () {
        $('#WeatherModal').load('/weather_widget').fadeToggle(1500);
        $("header").addClass("blur");
        $("main").addClass("blur");
    }

    window.onclick = function (event) {
        if (event.target == modal) {
            $("#WeatherModal").fadeToggle(750, function () {
                $("#WeatherModal").empty();
                $("header").removeClass("blur");
                $("main").removeClass("blur");
            });
        }
    }

});