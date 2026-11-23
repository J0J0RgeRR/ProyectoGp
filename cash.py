import bathrooms
import expenses


def validarMonto(value):
    amount, error = expenses.validarMonto(value)

    return amount, error

def abrirCaja():
    while True:
        amount, error = validarMonto(input("Ingrese el monto inicial de caja: C$"))

        if error is None:
            return amount
        else:
            print(error)

def validarCaja(currentCash, token):
    if currentCash is None:
        return "Primero abrí la caja desde Caja y gastos."

    if token != currentCash["token"]:
        return "La caja cambió. Recargá la página e intentá nuevamente."

    return None


def iniciarCaja(currentCash, value, sales, parkingTotal, merchantTotal, expenseRecords, token):
    if currentCash is not None:
        return currentCash, "Ya hay una caja abierta."

    amount, error = validarMonto(value)

    if error is not None:
        return None, error

    bathroomTotal = bathrooms.calcularTotalCobros(sales)
    expenseStart = len(expenseRecords)

    currentCash = {
        "initialAmount": amount,
        "bathroomStart": bathroomTotal,
        "parkingStart": parkingTotal,
        "merchantStart": merchantTotal,
        "expenseStart": expenseStart,
        "token": token
    }

    return currentCash, None


def calcularSaldo(initialAmount, totalIncome, totalExpenses):
    balance = initialAmount + totalIncome - totalExpenses
    balance = round(balance, 2)

    return balance


def calcularDiferencia(expectedBalance, countedCash):
    difference = countedCash - expectedBalance
    difference = round(difference, 2)

    return difference


def resumirCaja(initialAmount, bathroomIncome, parkingIncome, merchantIncome, totalExpenses):
    totalIncome = bathroomIncome + parkingIncome + merchantIncome
    totalIncome = round(totalIncome, 2)

    balance = calcularSaldo(initialAmount, totalIncome, totalExpenses)

    summary = {
        "initialAmount": initialAmount,
        "bathroomIncome": bathroomIncome,
        "parkingIncome": parkingIncome,
        "merchantIncome": merchantIncome,
        "totalIncome": totalIncome,
        "totalExpenses": totalExpenses,
        "balance": balance
    }

    return summary


def consultarResumen(currentCash, sales, parkingTotal, merchantTotal, expenseRecords):
    if currentCash is None:
        return None

    bathroomIncome = bathrooms.calcularTotalCobros(sales) - currentCash["bathroomStart"]
    parkingIncome = parkingTotal - currentCash["parkingStart"]
    merchantIncome = round(merchantTotal - currentCash["merchantStart"], 2)

    currentExpenses = expenseRecords[currentCash["expenseStart"]:]
    totalExpenses = expenses.calcularTotalGastos(currentExpenses)

    summary = resumirCaja(currentCash["initialAmount"], bathroomIncome, parkingIncome, merchantIncome, totalExpenses)

    return summary


def finalizarCaja(currentCash, cashClosings, value, summary):
    if currentCash is None:
        return None, "No hay una caja abierta."

    countedCash, error = validarMonto(value)

    if error is not None:
        return currentCash, error

    difference = calcularDiferencia(summary["balance"], countedCash)

    summary["countedCash"] = countedCash
    summary["difference"] = difference

    cashClosings.append(summary)

    return None, None

def cerrarCaja(expectedBalance):
    while True:
        countedCash, error = validarMonto(input("Ingrese el efectivo contado: C$"))

        if error is None:
            break
        else:
            print(error)

    difference = calcularDiferencia(expectedBalance, countedCash)

    print(f"Saldo esperado: C${expectedBalance:.2f}")
    print(f"Efectivo contado: C${countedCash:.2f}")

    if difference < 0:
        print(f"Faltan C${-difference:.2f}.")
    elif difference > 0:
        print(f"Sobran C${difference:.2f}.")
    else:
        print("La caja cuadra.")

    while True:
        print("1. Confirmar cierre")
        print("2. Cancelar")

        option = input("Seleccione una opción: ").strip()

        if option == "1":
            return countedCash, difference
        elif option == "2":
            return None
        else:
            print("Seleccione 1 o 2.")