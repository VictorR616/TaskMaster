function asignarColoresFondo() {
    const coloresFondo = ["#a328b9", "#3498db", "#27ae60", "#f1c40f", "#e74c3c"];
    const items = document.querySelectorAll(".content-item");

    items.forEach((item, index) => {
        const color = coloresFondo[index % coloresFondo.length];
        item.style.backgroundColor = color;
    });
}


document.addEventListener("DOMContentLoaded", function () {
    asignarColoresFondo();
});

