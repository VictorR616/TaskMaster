import dropdownMenu from "./dropdown.js";
import hamburgerMenu from "./hamburguer.js";

document.addEventListener("DOMContentLoaded", function () {
    dropdownMenu("dropdown-button", "myDropdown");
    hamburgerMenu(".hamburguer", ".panel", ".menu a");
});
