function setupDeleteModal() {
    const background_modal = document.getElementById("delete-task-modal");
    const cancelButton = document.getElementById("cancel-delete");
    const close = document.querySelector(".close");

    // Agrega un evento de clic al botón .btn-delete
    const deleteButton = document.querySelector(".btn-delete");
    deleteButton.addEventListener("click", () => {
        background_modal.style.display = "grid";
    });

    cancelButton.addEventListener("click", () => {
        background_modal.style.display = "none";
    });

    close.addEventListener("click", () => {
        background_modal.style.display = "none";
    });

    // Agrega un evento de clic al fondo oscuro (fuera del modal)
    window.addEventListener("click", (event) => {
        if (event.target === background_modal) {
            background_modal.style.display = "none";
        }
    });
}


// Llama a la función para configurar el modal de eliminación cuando la página se carga
document.addEventListener("DOMContentLoaded", setupDeleteModal);
