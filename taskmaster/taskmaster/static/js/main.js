document.addEventListener("DOMContentLoaded", function () {
    // Elementos DOM
    const dropdownButton = document.getElementById("dropdown-button");
    const dropdownContent = document.getElementById("myDropdown");
    const table = document.querySelector(".table");
    const cardContainer = document.querySelector(".card-container");

    // Función para cambiar la vista según el ancho de la pantalla
    function toggleView() {
        if (window.innerWidth <= 900) {
            table.style.display = "none";
            cardContainer.style.display = "flex";
        } else {
            table.style.display = "table";
            cardContainer.style.display = "none";
        }
    }

    // Evento de carga inicial y cambio de tamaño de ventana
    toggleView();
    window.addEventListener("resize", toggleView);

    // Evento de clic en el botón desplegable
    dropdownButton.addEventListener("click", function () {
        dropdownContent.classList.toggle("show");
    });

    // Evento para cerrar el menú al hacer clic fuera de él
    window.addEventListener("click", function (event) {
        if (!event.target.matches("#dropdown-button")) {
            const dropdowns = document.getElementsByClassName("dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.classList.contains("show")) {
                    openDropdown.classList.remove("show");
                }
            }
        }
    });
});
