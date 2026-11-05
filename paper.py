def ingresarRollos():
    while True:
        try:
            rolls = int(input("Cantidad de rollos que ingresan: "))

            if rolls > 0:
                units = rolls * 18
                return units
            else:
                print("La cantidad debe ser mayor que cero.")

        except ValueError:
            print("Debe ingresar un número entero.")