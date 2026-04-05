// Arreglo de productos
const productos = [
    {
        nombre: "Laptop",
        precio: 800,
        descripcion: "Equipo portátil para estudio y trabajo"
    },
    {
        nombre: "Mouse Inalámbrico",
        precio: 15,
        descripcion: "Mouse ergonómico y recargable"
    },
    {
        nombre: "Teclado Mecánico",
        precio: 25,
        descripcion: "Teclado con retroiluminación básica"
    }
];

// Referencias al DOM
const lista = document.getElementById("listaProductos");
const boton = document.getElementById("btnAgregar");

// Función para mostrar productos
function renderizarProductos() {
    lista.innerHTML = "";

    productos.forEach(producto => {
        const li = document.createElement("li");

        li.innerHTML = `
            <strong>${producto.nombre}</strong><br>
            <span class="precio">$${producto.precio}</span><br>
            <small>${producto.descripcion}</small>
        `;

        lista.appendChild(li);
    });
}

// Evento del botón
boton.addEventListener("click", () => {
    const nombre = document.getElementById("nombre").value;
    const precio = document.getElementById("precio").value;
    const descripcion = document.getElementById("descripcion").value;

    if (nombre === "" || precio === "" || descripcion === "") {
        alert("Por favor, complete todos los campos");
        return;
    }

    const nuevoProducto = {
        nombre: nombre,
        precio: precio,
        descripcion: descripcion
    };

    productos.push(nuevoProducto);
    renderizarProductos();

    // Limpiar campos
    document.getElementById("nombre").value = "";
    document.getElementById("precio").value = "";
    document.getElementById("descripcion").value = "";
});

// Mostrar productos al cargar la página
renderizarProductos();
