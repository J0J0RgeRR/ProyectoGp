def solicitarMonto():
    while True:
        try:
            amount= float(input("Ingrese el monto del gasto: C$"))

            if amount > 0:
                return amount
            else:
                print("El monto debe ser mayor que cero.")

        except ValueError:
            print("Debe ingresar un número valido.")