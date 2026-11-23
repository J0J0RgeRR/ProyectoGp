def validarMonto(value):
    try:
        amount = float(value)   

        if amount >= 0:
            amount = round(amount, 2)
            return amount, None
        else:
            return None, "El monto no puede ser negativo."

    except ValueError:
        return None, "Ingrese un número válido."


def solicitarDescripcion():
    while True:
        description = input("Descripción del gasto: ").strip()

        if description != "":
            return description

        print("Debe ingresar una descripción del gasto realizado.")


def guardarGasto(expenses, amount, description, balance=None):
    amount, error = validarMonto(amount)

    if error is not None:
        return False, error

    if amount <= 0:
        return False, "El monto mínimo es C$0.01."

    description = description.strip()

    if description == "":
        return False, "Debe ingresar una descripción del gasto."

    if balance is not None and amount > balance:
        return False, "El gasto supera el saldo disponible en caja."

    expense = {"amount": amount,"description": description}

    expenses.append(expense)

    return True, "Gasto registrado correctamente."


def calcularTotalGastos(expenses):
    total = 0

    for expense in expenses:
        total = total + expense["amount"]

    total = round(total, 2)

    return total


def solicitarMonto():
    while True:
        amount, error = validarMonto(input("Ingrese el monto del gasto: C$"))

        if error is None and amount > 0:
            return amount

        if error is not None:
            print(error)
        else:
            print("El monto debe ser mayor que cero.")

def confirmarGasto(amount, description):
    while True:
        print("--- CONFIRMAR GASTO ---")
        print(f"Monto: C${amount:.2f}")
        print(f"Descripción: {description}")
        print("1. Confirmar")
        print("2. Cancelar")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            return True
        elif option == "2":
            return False
        else:
            print("Seleccione una opción del 1 al 2.")


def registrarGasto(expenses):
    amount = solicitarMonto()
    description = solicitarDescripcion()
    confirmed = confirmarGasto(amount, description)

    if confirmed:
        saved, message = guardarGasto(expenses, amount, description)
        print(message)
    else:
        print("Gasto cancelado.")


def consultarGastos(expenses):
    if len(expenses) == 0:
        return "No hay gastos registrados."

    total = calcularTotalGastos(expenses)

    return expenses, total