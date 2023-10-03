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

function asignarColoresFondo() {
    const coloresFondo = ["#a328b9", "#3498db", "#27ae60", "#f1c40f", "#e74c3c"];
    const categorias = document.querySelectorAll(".categoria");

    categorias.forEach((categoria, index) => {
        const color = coloresFondo[index % coloresFondo.length];
        categoria.style.backgroundColor = color;
    });

}

document.addEventListener("DOMContentLoaded", function () {
    asignarColoresFondo();
    setupModal();
});

