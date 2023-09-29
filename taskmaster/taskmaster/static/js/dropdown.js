export default function dropdownMenu(dropdownButtonId, dropdownContentId) {
    // Elementos DOM
    const dropdownButton = document.getElementById(dropdownButtonId);
    const dropdownContent = document.getElementById(dropdownContentId);

    console.log("Hello")

    // Evento de clic en el botón desplegable
    dropdownButton.addEventListener("click", function () {
        dropdownContent.classList.toggle("show");
    });

    // Evento para cerrar el menú al hacer clic fuera de él
    window.addEventListener("click", function (event) {
        if (!event.target.matches(`#${dropdownButtonId}`)) {
            const dropdowns = document.getElementsByClassName("dropdown-content");
            for (let i = 0; i < dropdowns.length; i++) {
                const openDropdown = dropdowns[i];
                if (openDropdown.classList.contains("show")) {
                    openDropdown.classList.remove("show");
                }
            }
        }
    });
}
