$(document).ready(function () {

  $("#WeatherBlock").click(function () {
    $("main").addClass("blur");
    $('#WeatherModal').load('/weather_widget').fadeToggle(1500);
  });

  $("#WeatherModal").click(function () {

    $("#WeatherModal").fadeToggle(750, function () {
      $("#WeatherModal").empty();
      $("main").removeClass("blur");

    });

  });

});