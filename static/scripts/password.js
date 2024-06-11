function togglePasswordVisibility() {
    event.preventDefault();
    var passwordInput = document.getElementById('password-input');
    var set_text_button = document.querySelector('.set_text_button');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        set_text_button.textContent = 'Скрыть пароль';
        
    } else {
        passwordInput.type = 'password';
        set_text_button.textContent = 'Показать пароль';

    }
}
function togglePasswordVisibility1() {
  event.preventDefault();
  var passwordInput = document.getElementById('password2');
  var set_text_button = document.querySelector('.set_text_button');
  
  if (passwordInput.type === 'password') {
      passwordInput.type = 'text';
      set_text_button.textContent = 'Скрыть пароль';
      
  } else {
      passwordInput.type = 'password';
      set_text_button.textContent = 'Показать пароль';

  }
}
var toggleButtons = document.querySelectorAll('.toggleButton');


toggleButtons.forEach(function(button) {
  
  button.addEventListener('click', function(event) {
    event.preventDefault();


    var targetFormId = this.getAttribute('data-form');
    var targetForm = document.getElementById(targetFormId);


    document.querySelectorAll('.frame-2').forEach(function(form) {
      form.style.display = 'none';
    });

    targetForm.style.display = 'inline-flex';
  });
});


function checkPasswords(event) {
  event.preventDefault();
  var password1 = document.getElementById('password1').value;
  var password2 = document.getElementById('password2').value;
  var inputPassword1 = document.getElementById('password1');
  var inputPassword2 = document.getElementById('password2');

  if (password1 !== password2) {
    inputPassword1.style.border = '1px solid darkred';
    inputPassword2.style.border = '1px solid darkred';
    return false;
  } else {
    inputPassword1.style.border = '1px solid #ccc';
    inputPassword2.style.border = '1px solid #ccc';
    var button = document.getElementById('submitBtnPass');
    var loader = document.getElementById('loader_pass');
  
    button.style.display = 'none';
    loader.style.display = 'inline-block';
    document.getElementById('set_two').submit();
  
  }
}

function replaceWithLoader() {
  var button = document.getElementById('submitBtn');
  var loader = document.getElementById('loader');

  button.style.display = 'none';
  loader.style.display = 'inline-block';
}