// Add review button

const reviewButton = document.querySelector('#add-review');
if (reviewButton) {
    reviewButton.addEventListener('click', function () {
        window.location.href = '/add-review/';
    });
}
    