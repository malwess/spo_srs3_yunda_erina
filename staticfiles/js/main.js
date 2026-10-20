// Включение всплывающих подсказок Bootstrap на всех страницах
document.addEventListener("DOMContentLoaded", function () {
    const items = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    items.forEach(function (item) {
        new bootstrap.Tooltip(item);
    });
});
