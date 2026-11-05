class Nodo:
    def __init__(self, identificador, tipo, modalidad, cantidad, precio_unitario, total):
        self.identificador = identificador
        self.tipo = tipo
        self.modalidad = modalidad
        self.cantidad = cantidad
        self.precio_unitario = precio_unitario
        self.total = total
        self.siguiente = None