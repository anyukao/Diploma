

    const fileIcons = {
        'pdf': '/static/images/icons/pdf-icon1.png',
        'xlsx': '/static/images/icons/excel-icon1.png',
        'xls': '/static/images/icons/excel-icon1.png',
        'pptx': '/static/images/icons/powerpoint-icon1.png',
        'ppt': '/static/images/icons/powerpoint-icon1.png',
        'docx': '/static/images/icons/word-icon6.png',
        'doc': '/static/images/icons/word-icon6.png',
        'jpg': '/static/images/icons/image-icon.png',
        'jpeg': '/static/images/icons/image-icon.png',
        'png': '/static/images/icons/image-icon.png',
        'gif': '/static/images/icons/image-icon.png',
        'default': '/static/images/icons/file.png',
        'txt': '/static/images/icons/file.png',
        'mp4': '/static/images/icons/mp4-icon.png',
    };

    document.addEventListener('DOMContentLoaded', function () {
        const fileItems = document.querySelectorAll('.file-icon');
        
        fileItems.forEach(item => {
            const fileName = item.getAttribute('data-file-name');
            const extension = fileName.split('.').pop().toLowerCase();
            const iconSrc = fileIcons[extension] || fileIcons['default'];
            item.src = iconSrc;
        });
    });