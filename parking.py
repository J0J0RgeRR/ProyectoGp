def seleccionar_servicio():
    while True:
        print("\n========== SERVICIOS DE PARQUEO ==========")
        print("1. Parqueo de moto")
        print("2. Parqueo de vehículo")
        print("3. Volver")


        try:
            option = int(input("Seleccione una opción: "))


            if option == 1:
                seleccionar_modalidad("MOTO")


            elif option == 2:
                seleccionar_modalidad("VEHÍCULO")


            elif option == 3:
                return


            else:
                print("Seleccione una opción del 1 al 3.")


        except ValueError:
            print("Debe ingresar un número entero.")




def seleccionar_modalidad(tipo):
    while True:
        print(f"\n========== PARQUEO DE {tipo} ==========")
        print("1. Parqueo por un rato")
        print("2. Parqueo todo el día")
        print("3. Volver")


        try:
            option = int(input("Seleccione una modalidad: "))


            if option == 1:
                print(f"Seleccionó parqueo de {tipo.lower()} por un rato.")


            elif option == 2:
                print(f"Seleccionó parqueo de {tipo.lower()} todo el día.")


            elif option == 3:
                return


            else:
                print("Seleccione una opción del 1 al 3.")


        except ValueError:
            print("Debe ingresar un número entero.")


