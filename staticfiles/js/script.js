document.addEventListener('DOMContentLoaded', function() {
    handleAddReviewButton();
    handleEditReviewButton();
    if (document.querySelector('#delete-review')) {
        handleDeleteModal();
    }
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

// Trigger delete modal and set delete confirm button to delete review url
function handleDeleteModal() {
    const deleteModalButton = document.querySelector('#delete-review')
    const deleteModal = new bootstrap.Modal(document.querySelector('#delete-modal'));
    const deleteConfirmButton = document.querySelector('#delete-confirm');

    if (deleteModalButton && deleteModal) {
        const reviewPk = deleteModalButton.dataset.reviewPk;
        deleteModalButton.addEventListener('click', function() {
            deleteConfirmButton.setAttribute('href', `/my-reviews/delete/${reviewPk}/`);
            deleteModal.show();
        })
    }
}



