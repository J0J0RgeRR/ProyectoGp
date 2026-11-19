def validarMonto(value):
    try:
        amount = float(value)
    except (ValueError, TypeError):
        return None, "Ingrese un número válido."

    if not 0 <= amount < float("inf"):
        return None, "El monto debe ser finito y mayor o igual a cero."

    return round(amount, 2), None


def abrirCaja():
    while True:
        amount, error = validarMonto(
            input("Ingrese el monto inicial de caja: C$")
        )

        if error is None:
            return amount

        print(error)


def calcularSaldo(initialAmount, totalIncome, totalExpenses):
    return round(initialAmount + totalIncome - totalExpenses, 2)


def calcularDiferencia(expectedBalance, countedCash):
    return round(countedCash - expectedBalance, 2)

def cerrarCaja(expectedBalance):
    while True:
        countedCash, error = validarMonto(
            input("Ingrese el efectivo contado: C$")
        )

        if error is None:
            break

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

            
def resumirCaja(
    initialAmount,
    bathroomIncome,
    parkingIncome,
    merchantIncome,
    totalExpenses
):
    totalIncome = round(
        bathroomIncome + parkingIncome + merchantIncome, 2
    )

    return {
        "initialAmount": initialAmount,
        "bathroomIncome": bathroomIncome,
        "parkingIncome": parkingIncome,
        "merchantIncome": merchantIncome,
        "totalIncome": totalIncome,
        "totalExpenses": totalExpenses,
        "balance": calcularSaldo(
            initialAmount, totalIncome, totalExpenses
        )
    }