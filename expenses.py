def guardarGasto(expenses, amount, description):
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return False, "Debe ingresar un número válido."

    if not amount > 0 or amount == float("inf"):
        return False, "El monto debe ser un número positivo y finito."

    amount = round(amount, 2)

    if amount == 0:
        return False, "El monto mínimo es C$0.01."

    description = description.strip()

    if description == "":
        return False, "Debe ingresar una descripción del gasto."

    expense = {
        "amount": amount,
        "description": description
    }

    expenses.append(expense)
    return True, "Gasto registrado correctamente."


def solicitarMonto():
    while True:
        try:
            amount = float(input("Ingrese el monto del gasto: C$"))

            if amount > 0:
                return amount

            print("El monto debe ser mayor que cero.")

        except ValueError:
            print("Debe ingresar un número válido.")


def solicitarDescripcion():
    while True:
        description = input("Descripción del gasto: ").strip()

        if description != "":
            return description

        print("Debe ingresar una descripción del gasto realizado.")


def confirmarGasto(amount, description):
    while True:
        print("\n--- CONFIRMAR GASTO ---")
        print(f"Monto: C${amount:.2f}")
        print(f"Descripción: {description}")
        print("1. Confirmar")
        print("2. Cancelar")

        try:
            option = int(input("Seleccione una opción: "))

            if option == 1:
                return True
            elif option == 2:
                return False

            print("Seleccione una opción del 1 al 2.")

        except ValueError:
            print("Debe ingresar un número entero.")


def registrarGasto(expenses):
    amount = solicitarMonto()
    description = solicitarDescripcion()

    if confirmarGasto(amount, description):
        saved, message = guardarGasto(expenses, amount, description)
        print(message)
    else:
        print("Gasto cancelado.")


def consultarGastos(expenses):
    if len(expenses) == 0:
        return "No hay gastos registrados."

    total = 0

    for expense in expenses:
        total += expense["amount"]

    return expenses, total