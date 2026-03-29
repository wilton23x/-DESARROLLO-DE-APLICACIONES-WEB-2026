class Producto:

    def __init__(self, id, nombre, autor, cantidad, precio):
        self.id = id
        self.nombre = nombre
        self.autor = autor
        self.cantidad = cantidad
        self.precio = precio

    def __repr__(self):
        return f"<Producto {self.id} - {self.nombre}>"
    

class Inventario:

    def __init__(self):
        self.productos = {}

    # ======================
    # AGREGAR PRODUCTO
    # ======================
    def agregar_producto(self, producto):
        if producto.id in self.productos:
            print("⚠️ Producto ya existe, se sobrescribirá")
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
        return [
            producto for producto in self.productos.values()
            if nombre.lower() in producto.nombre.lower()
        ]

    # ======================
    # ELIMINAR PRODUCTO
    # ======================
    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
            return True
        return False