class ProductoForm:
    def __init__(self, form):
        self.nombre = form.get("nombre")
        self.autor = form.get("autor")
        self.cantidad = form.get("cantidad")
        self.precio = form.get("precio")

    def validar(self):
        errores = []

        if not self.nombre:
            errores.append("El nombre es obligatorio")

        if not self.precio:
            errores.append("El precio es obligatorio")

        try:
            if float(self.precio) <= 0:
                errores.append("El precio debe ser mayor a 0")
        except:
            errores.append("El precio debe ser numérico")

        return errores