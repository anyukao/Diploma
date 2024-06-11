document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const courseItems = document.querySelectorAll('#results .item');

    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        
        courseItems.forEach(function(item) {
            const courseName = item.textContent.toLowerCase();
            if (courseName.includes(filter)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
});