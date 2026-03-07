class Producto:

    def __init__(self, id, nombre, autor, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.autor = autor
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        return f"<Producto {self.nombre}>"


class Inventario:

    def __init__(self):
        # Diccionario {id: Producto}
        self.productos = {}

    # Agregar producto al inventario
    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    # Mostrar todos los productos
    def mostrar_todos(self):
        return list(self.productos.values())

    # Buscar producto por nombre
    def buscar_por_nombre(self, nombre):

        resultados = []

        for producto in self.productos.values():
            if nombre.lower() in producto.nombre.lower():
                resultados.append(producto)

        return resultados