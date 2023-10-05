export default function setupModal(deleteButton) {
    const showButton = document.getElementById("delete-task-modal");
    const cancelButton = document.getElementById("cancel-delete");

    deleteButton.addEventListener("click", showModal);
    cancelButton.addEventListener("click", hideModal);

    // Agrega un evento de clic al fondo oscuro (fuera del modal)
    window.addEventListener("click", (event) => {
        if (event.target === showButton) {
            hideModal();
        }
    });

    function showModal() {
        showButton.style.display = "grid";
    }

    function hideModal() {
        showButton.style.display = "none";
    }
}
