var modal2 = document.getElementById("myModal2");
var closeButton2 = document.querySelector(".close2");
const sumbitapp = document.getElementById('sumbitapp');
function openModal() {
  modal2.style.display = "block";
}

closeButton2.addEventListener("click", function() {
  modal2.style.display = "none"; // Скрываем модальное окно
});

window.addEventListener("click", function(event) {
  if (event.target === modal2) {
    modal2.style.display = "none"; // Скрываем модальное окно
  }
});