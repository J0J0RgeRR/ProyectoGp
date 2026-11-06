import bathrooms
import paper

stock = 18

while True:
    print("-- PRUEBAS ---")
    print("1. Registrar cobro")
    print("2. Consultar inventario")
    print("3. Salir")

    try:
        option = int(input("Seleccione una opción: "))

        if option == 1:
            stock = bathrooms.registrarCobro(stock)

        elif option == 2:
            paper.consultarInventario(stock)

        elif option == 3:
            break

        else:
            print("Seleccione una opción del 1 al 3.")

    except ValueError:
        print("Debe ingresar un número entero.")