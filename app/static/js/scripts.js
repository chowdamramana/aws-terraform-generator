document.addEventListener('htmx:beforeRequest', function(event) {
    const target = event.detail.target;
    target.innerHTML = '<div class="spinner mx-auto"></div>';
});

document.addEventListener('htmx:afterSwap', function(event) {
    Prism.highlightAll();
});

function validateField(field) {
    if (field.required && !field.value) {
        field.classList.add('border-red-500');
    } else {
        field.classList.remove('border-red-500');
    }
}