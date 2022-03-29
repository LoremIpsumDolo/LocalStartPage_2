$(document).ready(function () {

    const TimerInterval = 2000;

    Timer();

    function Timer() {
        updateClock();
        setTimeout(Timer, TimerInterval)
    }

    //	CLOCK

    function updateClock() {
        // console.log("checking clock");
        const date = new Date();
        const today = new Date();
        const days = ["Sonnatg", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
        const month = today.getMonth() + 1;
        const day = today.getDate();
        const year = today.getFullYear();

        document.getElementById('clock').innerHTML = date.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit'
        });
        document.getElementById("day").innerHTML = days[today.getDay()];
        document.getElementById("date_date").innerHTML = day + "/" + month + "/" + year;
    }

});