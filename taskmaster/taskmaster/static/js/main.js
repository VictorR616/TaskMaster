import dropdownMenu from "./dropdown.js";
import hamburgerMenu from "./hamburguer.js";

document.addEventListener("DOMContentLoaded", () => {
    dropdownMenu("dropdown-button", "myDropdown");
    hamburgerMenu(".hamburguer", ".panel", ".menu a");

    console.log("Hola desde el main")
});
