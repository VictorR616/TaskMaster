import hamburgerMenu from "./hamburguer.js";
import setupModal from "./modal.js";

document.addEventListener("DOMContentLoaded", () => {
    hamburgerMenu();
    
    const deleteButton = document.getElementById("delete-modal");
    
    if (deleteButton) {
        setupModal(deleteButton);
    }
});


