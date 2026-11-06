import paper 

def seleccionarServicio():
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

def calcularPrecio(option):
    if option == 1:
        price = 10
    elif option == 2:
        price = 20
    elif option == 3:
        price= 5
    else:
        return None

    return price 

def confirmarCobro(price):
    while True:
        print(f"Total a pagar: C${price}")
        print("1. Confirmar")
        print("2. Cancelar")

        try:
            option= int(input("Seleccione una opcion:  "))
            if option == 1:
                return True
            elif option == 2:
                return False
            else:
                print("Seleccione una opcion 1|2.")
        except ValueError:
            print("Debe ingresar un número entero")

def registrarCobro(stock):
    option= seleccionarServicio()
    if option == 4:
        return stock

    price= calcularPrecio(option)

    if option == 1:
        units = 1
    elif option == 2:
        units = 2
    else: 
        units = 0

    if stock < units:
        print(f"No hay suficiente papel. Disponible: {stock} unidades")
        return stock

    confirmed= confirmarCobro(price)

    if confirmed:
        stock= paper.descontarPapel(stock, units)
        print(f"Cobro confirmado: C${price}")
    else:
        print("Cobro cancelado. No se descontó papel.")

    return stock
