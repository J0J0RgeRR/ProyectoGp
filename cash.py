def abrirCaja():
    while True:
        try:
            amount = float(input("Ingrese el monto inicial de caja: C$"))

            if amount >= 0:
                return amount
            else:
                print("El monto inicial debe ser mayor o igual a cero.")

        except ValueError:
            print("Debe ingresar un número válido.")

def calcularSaldo(initialAmount, totalIncome, totalExpenses):
    balance= initialAmount + totalIncome -  totalExpenses
    return balance