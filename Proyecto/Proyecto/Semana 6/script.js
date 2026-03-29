const nombre = document.getElementById("nombre");
const correo = document.getElementById("correo");
const password = document.getElementById("password");
const confirmar = document.getElementById("confirmar");
const edad = document.getElementById("edad");
const btnEnviar = document.getElementById("btnEnviar");

function validarFormulario() {
    let valido = true;

    // Nombre
    if (nombre.value.length < 3) {
        errorNombre.textContent = "Mínimo 3 caracteres";
        nombre.className = "invalido";
        valido = false;
    } else {
        errorNombre.textContent = "";
        nombre.className = "valido";
    }

    // Correo
    const regexCorreo = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!regexCorreo.test(correo.value)) {
        errorCorreo.textContent = "Correo no válido";
        correo.className = "invalido";
        valido = false;
    } else {
        errorCorreo.textContent = "";
        correo.className = "valido";
    }

    // Contraseña
    const regexPass = /^(?=.*\d)(?=.*[!@#$%^&*]).{8,}$/;
    if (!regexPass.test(password.value)) {
        errorPassword.textContent = "Mínimo 8 caracteres, número y símbolo";
        password.className = "invalido";
        valido = false;
    } else {
        errorPassword.textContent = "";
        password.className = "valido";
    }

    // Confirmación
    if (confirmar.value !== password.value) {
        errorConfirmar.textContent = "Las contraseñas no coinciden";
        confirmar.className = "invalido";
        valido = false;
    } else {
        errorConfirmar.textContent = "";
        confirmar.className = "valido";
    }

    // Edad
    if (edad.value < 18) {
        errorEdad.textContent = "Debe ser mayor de edad";
        edad.className = "invalido";
        valido = false;
    } else {
        errorEdad.textContent = "";
        edad.className = "valido";
    }

    btnEnviar.disabled = !valido;
}

document.querySelectorAll("input").forEach(input => {
    input.addEventListener("input", validarFormulario);
});

document.getElementById("registroForm").addEventListener("submit", e => {
    e.preventDefault();
    alert("Formulario enviado correctamente");
});
const errorNombre = document.getElementById("errorNombre");