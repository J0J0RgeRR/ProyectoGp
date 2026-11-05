def seleccionar_servicio():
    while True:
        print("\n--- SERVICIOS DE BAÑOS ---")
        print("1. Sanitario: 1 unidad")
        print("2. Sanitario: 2 unidades")
        print("3. Urinario para varones")
        print("4. Volver")

        try:
            option = int(input("Seleccione una opción: "))

            if option >= 1 and option <= 4:
                return option
            else:
                print("Seleccione una opción del 1 al 4.")

        except ValueError:
            print("Debe ingresar un número entero.")