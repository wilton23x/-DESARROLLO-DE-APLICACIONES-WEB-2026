class Producto:
    def __init__(self, id, nombre, autor, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.autor = autor
        self.cantidad = cantidad
        self.precio = precio


class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario {id: Producto}

    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    def mostrar_todos(self):
        return list(self.productos.values())

    def buscar_por_nombre(self, nombre):
        return [
            p for p in self.productos.values()
            if nombre.lower() in p.nombre.lower()
        ]