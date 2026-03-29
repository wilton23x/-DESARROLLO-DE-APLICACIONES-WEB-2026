const imageUrlInput = document.getElementById("imageUrl");
const addImageBtn = document.getElementById("addImage");
const deleteImageBtn = document.getElementById("deleteImage");
const gallery = document.getElementById("gallery");

let selectedImage = null;

// Agregar imagen
addImageBtn.addEventListener("click", () => {
    const url = imageUrlInput.value.trim();

    if (url === "") {
        alert("Por favor ingresa una URL válida");
        return;
    }

    const img = document.createElement("img");
    img.src = url;

    // Evento click para seleccionar imagen
    img.addEventListener("click", () => {
        selectImage(img);
    });

    gallery.appendChild(img);
    imageUrlInput.value = "";
});

// Seleccionar imagen
function selectImage(img) {
    if (selectedImage) {
        selectedImage.classList.remove("selected");
    }
    selectedImage = img;
    selectedImage.classList.add("selected");
}

// Eliminar imagen seleccionada
deleteImageBtn.addEventListener("click", () => {
    if (!selectedImage) {
        alert("No hay ninguna imagen seleccionada");
        return;
    }
    gallery.removeChild(selectedImage);
    selectedImage = null;
});

// Evento de teclado (Enter para agregar imagen)
imageUrlInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        addImageBtn.click();
    }
});
