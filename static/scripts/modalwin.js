// Получаем элементы
var modal = document.getElementById("myModal");
var img = document.getElementById("userImage");
var closeButton = document.querySelector(".close");

// Добавляем обработчик события клика на изображение
img.addEventListener("click", function() {
  modal.style.display = "block"; // Показываем модальное окно
});

// Добавляем обработчик события клика на кнопку закрытия
closeButton.addEventListener("click", function() {
  modal.style.display = "none"; // Скрываем модальное окно
});

// Закрытие модального окна при клике вне него
window.addEventListener("click", function(event) {
  if (event.target === modal) {
    modal.style.display = "none"; // Скрываем модальное окно
  }
});
