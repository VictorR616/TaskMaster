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
});

