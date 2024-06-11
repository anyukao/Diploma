document.querySelector(".search-filter").addEventListener("change", function() {
    var filter = this.value; /* Значение выбранного фильтра */
    var items = document.querySelectorAll("#results .item"); /* Получаем все элементы для фильтрации */
  
    items.forEach(function(item) {
      if (filter === "all" || item.getAttribute("data-status") === filter) {
        item.style.display = "block"; /* Показываем элементы, которые соответствуют фильтру */
      } else {
        item.style.display = "none"; /* Скрываем элементы, которые не соответствуют фильтру */
      }
    });
  });
 
 
  