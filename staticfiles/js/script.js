document.addEventListener('DOMContentLoaded', function() {
    handleAddReviewButton();
    handleEditReviewButton();
})

// Add-review button
function handleAddReviewButton() {
    const reviewButton = document.querySelector('#add-review');
    if (reviewButton) {
        reviewButton.addEventListener('click', function () {
        window.location.href = '/add-review/';
    });
    }
}

// Edit-review button
function handleEditReviewButton() {
    const editButton = document.querySelector('#edit-review');
    if (editButton) {
        const reviewPk = editButton.dataset.reviewPk;
        editButton.addEventListener('click', function () {
            window.location.href = `/my-reviews/edit/${reviewPk}/`;
        });
    }
}



