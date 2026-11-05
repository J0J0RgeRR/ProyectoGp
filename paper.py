def ingresarRollos(stock):
    while True:
        try:
            rolls = int(input("Cantidad de rollos que ingresan: "))

            if rolls > 0:
                units = rolls * 18
                stock = stock + units

                print(f"Se agregaron {units} unidades.")
                return stock
            else:
                print("La cantidad debe ser mayor que cero.")

        except ValueError:
            print("Debe ingresar un número entero.")


def descontarPapel(stock, units):
    if units < 0:
        print("La cantidad que se descontará no puede ser negativa.")
        return stock

    if stock < units:
        print("No hay suficiente papel.")
        return stock

    return stock - units