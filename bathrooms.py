import paper


def seleccionarServicio():
    while True:
        print("--- SERVICIOS DE BAÑOS ---")
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
        price = 5
    else:
        return None

    return price


def guardarCobro(stock, sales, option):
    try:
        option = int(option)
    except (ValueError, TypeError):
        return stock, False, "Seleccioná un servicio válido."

    price = calcularPrecio(option)

    if price is None:
        return stock, False, "Seleccioná un servicio válido."

    if option == 1:
        service = "Sanitario: 1 unidad"
        units = 1
    elif option == 2:
        service = "Sanitario: 2 unidades"
        units = 2
    else:
        service = "Urinario para varones"
        units = 0

    if stock < units:
        return stock, False, "No hay suficiente papel para registrar este servicio."

    stock = paper.descontarPapel(stock, units)

    sale = {  "service": service,"price": price}

    sales.append(sale)

    message = f"Cobro confirmado: C${price:.2f}"

    return stock, True, message


def confirmarCobro(price):
    while True:
        print(f"Total a pagar: C${price}")
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


def registrarCobro(stock, sales):
    option = seleccionarServicio()

    if option == 4:
        return stock

    price = calcularPrecio(option)
    confirmed = confirmarCobro(price)

    if confirmed:
        stock, saved, message = guardarCobro(stock, sales, option)
        print(message)
    else:
        print("Cobro cancelado. No se descontó papel.")

    return stock


def calcularTotalCobros(sales):
    total = 0

    for sale in sales:
        total = total + sale["price"]

    return total


def consultarCobros(sales):
    if len(sales) == 0:
        print("No hay cobros registrados.")
        return

    print("========== HISTORIAL DE BAÑOS ==========")

    for sale in sales:
        print(f"{sale['service']}: C${sale['price']}")

    total = calcularTotalCobros(sales)

    print(f"Total recibido: C${total}")