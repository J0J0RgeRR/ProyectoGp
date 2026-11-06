import bathrooms
import paper

stock = 18
sales = []

while True:
    print("\n--- PRUEBAS ---")
    print("1. Registrar cobro")
    print("2. Consultar inventario")
    print("3. Consultar cobros")
    print("4. Salir")

    try:
        option = int(input("Seleccione una opción: "))

        if option == 1:
            stock = bathrooms.registrarCobro(stock, sales)

        elif option == 2:
            paper.consultarInventario(stock)

        elif option == 3:
            bathrooms.consultarCobros(sales)

        elif option == 4:
            break

        else:
            print("Seleccione una opción del 1 al 4.")

    except ValueError:
        print("Debe ingresar un número entero.")