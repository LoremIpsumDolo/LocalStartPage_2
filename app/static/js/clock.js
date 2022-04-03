$(document).ready(function () {

  const TimerInterval = 2000;

  Timer();

  function Timer() {
    updateClock();
    setTimeout(Timer, TimerInterval)
  }

  //	CLOCK

  function updateClock() {
    const date = new Date();
    const today = new Date();
    const days = ["Sonnatg", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
    const month = today.getMonth() + 1;
    const day = today.getDate();
    const year = today.getFullYear();

    document.getElementById('clock_time').innerHTML = date.toLocaleTimeString([], {
      hour  : '2-digit',
      minute: '2-digit'
    });
    document.getElementById("clock_day").innerHTML = days[today.getDay()];
    document.getElementById("clock_date").innerHTML = day + "/" + month;
  }

});