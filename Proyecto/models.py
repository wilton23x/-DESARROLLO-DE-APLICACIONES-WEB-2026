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
        # Diccionario donde la clave es el id
        self.productos = {}

    # ======================
    # AGREGAR PRODUCTO
    # ======================
    def agregar_producto(self, producto):
        self.productos[producto.id] = producto

    # ======================
    # MOSTRAR TODOS
    # ======================
    def mostrar_todos(self):
        return list(self.productos.values())

    # ======================
    # BUSCAR POR NOMBRE
    # ======================
    def buscar_por_nombre(self, nombre):

        resultados = []

        for producto in self.productos.values():
            if nombre.lower() in producto.nombre.lower():
                resultados.append(producto)

        return resultados

    # ======================
    # ELIMINAR PRODUCTO
    # ======================
    def eliminar_producto(self, id):

        if id in self.productos:
            del self.productos[id]