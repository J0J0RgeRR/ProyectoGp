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

def solicitarDescripcion():
    while True:
        description= input("Descripcion del gasto: ").strip()

        if description != "":
            return description
        else:
            print("Debe ingresar una descripcion del gasto realizado.")

def confirmarGasto(amount, description):
    while True:
        print("--- CONFIRMAR GASTO ---")
        print(f"Monto: C${amount}")
        print(f"Descripción: {description}")
        print("1. Confirmar")
        print("2. Cancelar")

        try:
            option = int(input("Seleccione una opción: "))

            if option == 1:
                return True
            elif option == 2:
                return False
            else:
                print("Seleccione una opción del 1 al 2.")

        except ValueError:
            print("Debe ingresar un número entero.")