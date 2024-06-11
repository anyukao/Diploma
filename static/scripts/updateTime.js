
    function updateTime() {
        var now = new Date();
        var hours = now.getHours();
        var minutes = now.getMinutes();
    

        var timeString = hours + ':' + minutes
        document.getElementById('clock').innerText = timeString;
    }

    setInterval(updateTime, 1000); // Обновление каждую секунду
    updateTime(); // Вызов функции сразу для отображения времени при загрузке страницы

