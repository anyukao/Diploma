function updateTextField() {
    const dateField = document.getElementById('dateield');
    const textField = document.getElementById('textield');
    
    // Получаем значение даты из поля даты
    const selectedDate = dateField.value;
    
    // Устанавливаем это значение в текстовое поле
    textField.value = selectedDate;
}