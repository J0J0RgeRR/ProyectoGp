
from collections import deque

# Aquí guardamos las zonas de la plaza y sus conexiones
grafo = {}


# Agregamos una zona nueva a la plaza
def agregar_zona(grafo, zona):
    if zona not in grafo:
        grafo[zona] = []
        return True

    return False


# Conectamos dos zonas de la plaza
def conectar_zonas(grafo, origen, destino):
    if origen not in grafo or destino not in grafo:
        return False

    if origen == destino:
        return False

    if destino in grafo[origen]:
        return False

    grafo[origen].append(destino)
    grafo[destino].append(origen)

    return True


# Consultamos las zonas que tienen conexión directa
def consultar_zonas_conectadas(grafo, zona):
    if zona not in grafo:
        return None

    return grafo[zona][:]


# Revisamos si existe un camino directo entre dos zonas
def verificar_conexion(grafo, origen, destino):
    return origen in grafo and destino in grafo[origen]


# Mostramos las zonas y sus conexiones
def mostrar_conexiones(grafo):
    for zona, conexiones in grafo.items():
        print(zona, "->", conexiones)


# Buscamos el recorrido con menos tramos entre dos zonas
def buscarRuta(origen, destino):

    origen = origen.strip().upper()
    destino = destino.strip().upper()

    if origen not in grafo:
        print("\nError: la zona de origen no existe.")
        return None

    if destino not in grafo:
        print("\nError: la zona de destino no existe.")
        return None

    if origen == destino:
        return [origen]

    cola = deque([[origen]])
    visitados = {origen}

    while cola:

        ruta = cola.popleft()
        zona_actual = ruta[-1]

        for zona_vecina in consultar_zonas_conectadas(grafo, zona_actual):

            if zona_vecina not in visitados:

                nueva_ruta = ruta + [zona_vecina]

                if zona_vecina == destino:
                    return nueva_ruta

                visitados.add(zona_vecina)
                cola.append(nueva_ruta)

    print("\nNo existe un camino entre esas dos zonas.")
    return None


# Registramos las zonas y los caminos de la plaza
def crear_grafo():

    zonas = [
        "ENTRADA",
        "PARQUEO",
        "ADMINISTRACION",
        "BANOS",
        "COMEDOR"
    ]

    for zona in zonas:
        agregar_zona(grafo, zona)

    conexiones = [
        ("ENTRADA", "PARQUEO"),
        ("ENTRADA", "ADMINISTRACION"),
        ("PARQUEO", "BANOS"),
        ("ADMINISTRACION", "COMEDOR"),
        ("BANOS", "COMEDOR")
    ]

    for origen, destino in conexiones:
        conectar_zonas(grafo, origen, destino)


# Consultamos una ruta desde la terminal
def consultar_ruta():

    print("\n========== CONSULTA DE RUTAS ==========")

    print("\nZonas disponibles:")
    mostrar_conexiones(grafo)

    origen = input("\nIngrese la zona de origen: ")
    destino = input("Ingrese la zona de destino: ")

    ruta = buscarRuta(origen, destino)

    if ruta is not None:
        print("\n========== RUTA ENCONTRADA ==========")
        print("Recorrido:", " -> ".join(ruta))
        print("Cantidad de tramos:", len(ruta) - 1)


# Preparamos las zonas de la plaza
crear_grafo()


if __name__ == "__main__":
    consultar_ruta()
