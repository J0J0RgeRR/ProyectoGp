import random
import time

import merchants


# Generar mercaderes
def generarMercaderes(count):
    startTime = time.perf_counter()
    nodes = []
    width = max(6, len(str(count)))

    for number in range(1, count + 1):
        code = "A" + str(number).zfill(width)
        node = merchants.crearNodo(code, "Mercader " + str(number), "Venta de ropa", "88888888", 100, "diario")
        nodes.append(node)

    elapsedTime = time.perf_counter() - startTime
    return nodes, elapsedTime


# Mostrar datos
def mostrarMercader(node):
    print(f"Código: {node['local']} | Nombre: {node['name']} | Negocio: {node['business']} | Teléfono: {node['phone']} | Monto: C${node['rent']} | Modalidad: {node['frequency']}")


# Preparar árbol
def prepararArbol(nodes, case):
    merchants.root = None
    startTime = time.perf_counter()

    if case == "3":
        for index in range(len(nodes) - 1):
            nodes[index]["right"] = nodes[index + 1]

        merchants.root = nodes[0]
    else:
        random.Random(11).shuffle(nodes)

        for node in nodes:
            merchants.root = merchants.insertarNodo(merchants.root, node)

    elapsedTime = time.perf_counter() - startTime
    return elapsedTime


# Contar nodos visitados
def contarNodos(code):
    current = merchants.root
    visited = 0
    code = code.strip().upper()

    while current is not None:
        visited = visited + 1

        if code == current["local"]:
            return visited
        elif code < current["local"]:
            current = current["left"]
        else:
            current = current["right"]

    return visited


# Medir búsqueda
def medirBusqueda(code):
    totalTime = 0

    for repetition in range(5):
        startTime = time.perf_counter()
        found = merchants.buscarComerciante(code)
        elapsedTime = time.perf_counter() - startTime
        totalTime = totalTime + elapsedTime

    averageTime = totalTime / 5
    visited = contarNodos(code)

    return found, averageTime, visited


def main():
    try:
        count = int(input("Cantidad de mercaderes que desea generar: "))

        if count <= 0:
            print("Ingrese una cantidad mayor que cero.")
            return

        nodes, generationTime = generarMercaderes(count)
        firstCode = nodes[0]["local"]
        lastCode = nodes[-1]["local"]

        print("\nMercaderes generados:")

        for node in nodes:
            mostrarMercader(node)

        print(f"\nTotal de mercaderes: {count}")
        print(f"Códigos desde {firstCode} hasta {lastCode}")

        print("\nSeleccione el caso:")
        print("1. Mejor caso")
        print("2. Caso promedio")
        print("3. Peor caso")
        print("4. Buscar un código")

        case = input("Seleccione una opción: ").strip()

        if case not in ("1", "2", "3", "4"):
            print("Opción inválida.")
            return

        constructionTime = prepararArbol(nodes, case)

        if case == "1":
            codes = [merchants.root["local"]]
        elif case == "2":
            selectedNodes = random.Random(1011).sample(nodes, min(10, count))
            codes = []

            for node in selectedNodes:
                codes.append(node["local"])

        elif case == "3":
            codes = [lastCode]
        else:
            code = input("Código del mercader que desea buscar: ").strip().upper()
            codes = [code]

        results = []

        print("\nResultados de las búsquedas:")

        for code in codes:
            found, searchTime, visited = medirBusqueda(code)
            results.append((code, searchTime, visited))

            print(f"\nCódigo buscado: {code}")

            if found is not None:
                print("Mercader encontrado:")
                mostrarMercader(found)
            else:
                print("No se encontró el mercader.")

            print(f"Nodos visitados: {visited}")

        print("\nTiempos de la prueba:")
        print(f"Tiempo de generación: {generationTime:.6f} segundos")
        print(f"Tiempo de construcción del árbol: {constructionTime:.6f} segundos")

        totalTime = 0
        totalVisited = 0

        for code, searchTime, visited in results:
            print(f"Tiempo medio de búsqueda de {code}: {searchTime:.9f} segundos")
            totalTime = totalTime + searchTime
            totalVisited = totalVisited + visited

        print(f"\nPromedio de tiempo: {totalTime / len(results):.9f} segundos")
        print(f"Promedio de nodos visitados: {totalVisited / len(results):.2f}")
        print("Cada código se buscó cinco veces. Los tiempos no incluyen la impresión.")

    except ValueError:
        print("Ingrese una cantidad entera sin comas ni espacios.")
    except (MemoryError, RecursionError):
        print("No se pudo completar la prueba por falta de memoria o límite de recursión.")
    finally:
        merchants.root = None


if __name__ == "__main__":
    main()