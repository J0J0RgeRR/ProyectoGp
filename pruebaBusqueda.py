    import random
    import time

    import merchants


    # Generar registros completos sin guardarlos en los archivos del negocio.
    def generarMercaderes(count):
        startTime = time.perf_counter()
        nodes = []
        width = max(6, len(str(count)))

        for number in range(1, count + 1):
            code = "A" + str(number).zfill(width)
            node = merchants.crearNodo(code, "Mercader " + str(number),
                                    "Venta de ropa", "88888888", 100, "diario")
            nodes.append(node)

        elapsedTime = time.perf_counter() - startTime
        return nodes, elapsedTime


    # Preparar la entrada antes de medir la búsqueda.
    def prepararArbol(nodes, case):
        merchants.root = None
        startTime = time.perf_counter()

        if case == "3":
            # Cadena válida para el peor caso; no mide el registro normal.
            for index in range(len(nodes) - 1):
                nodes[index]["right"] = nodes[index + 1]
            merchants.root = nodes[0]
        else:
            random.Random(11).shuffle(nodes)
            for node in nodes:
                merchants.root = merchants.insertarNodo(merchants.root, node)

        return time.perf_counter() - startTime


    # Contar nodos aparte para no alterar el tiempo de la función original.
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


    # Repetir cinco veces y obtener el tiempo medio de la búsqueda real.
    def medirBusqueda(code):
        totalTime = 0

        for repetition in range(5):
            startTime = time.perf_counter()
            found = merchants.buscarComerciante(code)
            totalTime = totalTime + (time.perf_counter() - startTime)

        return found, totalTime / 5, contarNodos(code)


    def main():
        try:
            count = int(input("Ingrese la cantidad de mercaderes ficticios que desea generar para la prueba (ejemplo: 50000): "))
            if count <= 0:
                print("Ingrese una cantidad mayor que cero.")
                return

            print("1. Mejor caso\n2. Estimación del caso promedio")
            print("3. Peor caso\n4. Buscar un código escrito por usted")
            case = input("Seleccione una opción: ").strip()
            if case not in ("1", "2", "3", "4"):
                print("Opción inválida.")
                return

            nodes, generationTime = generarMercaderes(count)
            lastCode = nodes[-1]["local"]
            constructionTime = prepararArbol(nodes, case)
            print("\nMercaderes generados:", count)
            print("Códigos desde A000001 hasta", lastCode)
            print(f"Tiempo de generación: {generationTime:.6f} segundos")
            print(f"Tiempo de construcción del árbol: {constructionTime:.6f} segundos")

            if case == "1":
                codes = [merchants.root["local"]]
            elif case == "2":
                selectedNodes = random.Random(1011).sample(nodes, min(10, count))
                codes = [node["local"] for node in selectedNodes]
            elif case == "3":
                codes = [lastCode]
            else:
                print("Código de la raíz:", merchants.root["local"])
                codes = [input("Código del local que desea buscar: ").strip().upper()]

            totalTime = 0
            totalVisited = 0
            for code in codes:
                found, searchTime, visited = medirBusqueda(code)
                print("\nCódigo:", code, "| Encontrado:", found is not None)
                print("Nodos visitados:", visited)
                print(f"Tiempo medio de búsqueda: {searchTime:.9f} segundos")
                totalTime = totalTime + searchTime
                totalVisited = totalVisited + visited

            print(f"\nPromedio de nodos visitados: {totalVisited / len(codes):.2f}")
            print(f"Promedio de tiempo: {totalTime / len(codes):.9f} segundos")
            print("Cada código se midió cinco veces. Generación y construcción se miden aparte.")

        except ValueError:
            print("Ingrese una cantidad entera válida, sin comas ni espacios.")
        except (MemoryError, RecursionError):
            print("No se completó la prueba por un límite de memoria o recursión.")
        finally:
            merchants.root = None


    if __name__ == "__main__":
        main()
