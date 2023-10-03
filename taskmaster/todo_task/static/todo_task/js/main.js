
function setupModal() {
    const openModalBtn = document.querySelector(".open-modal-btn");
    const modal = document.querySelector(".modal");
    const closeModalBtn = document.querySelector(".close-modal-btn");

    function openModal() {
        modal.style.display = "grid";
    }

    function closeModal() {
        modal.style.display = "none";
    }

    openModalBtn.addEventListener("click", openModal);

    closeModalBtn.addEventListener("click", closeModal);

    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            closeModal();
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    setupModal();
});
