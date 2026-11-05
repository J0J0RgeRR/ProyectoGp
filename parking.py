class Nodo:
    def __init__(self, identificador, tipo, modalidad, cantidad, precio_unitario, total):
        self.identificador = identificador
        self.tipo = tipo
        self.modalidad = modalidad
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total
        self.siguiente = None

class ListaEnlazada:
    def __init__(self):
        self.cabeza = None

    def agregar(self, nuevo_nodo):
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
        else:
            actual = self.cabeza

            while actual.siguiente is not None:
                actual = actual.siguiente

            actual.siguiente = nuevo_nodo