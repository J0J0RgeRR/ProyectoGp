from collections import deque
from datetime import date

TARIFAS = {
    "MOTO": {"RATO": 20, "DIA": 30},
    "BICICLETA": {"RATO": 10, "DIA": 20},
    "CARRO": {"RATO": 30, "DIA": 50}
}

pendientes = deque()
cabeza = None
nextTicket = 1


def registrarPendiente(vehicleType, mode, identifier):
    global nextTicket

    if vehicleType not in TARIFAS or mode not in ("RATO", "DIA"):
        return "Seleccioná un vehículo y una modalidad válidos."

    identifier = identifier.strip().upper()

    if identifier == "":
        return "La identificación no puede estar vacía."

    if vehicleType == "BICICLETA" and mode == "RATO":
        if not identifier.replace(" ", "").isalpha():
            return "El color de la bicicleta solo debe contener letras."

    pendientes.append({
        "identificador": identifier,
        "tipo": vehicleType,
        "modalidad": mode,
        "webToken": str(nextTicket)
    })

    nextTicket += 1
    return None


def calcularCobro(vehicleType, mode, quantity=1):
    if vehicleType not in TARIFAS or mode not in ("RATO", "DIA"):
        return None, "Vehículo o modalidad no válidos."

    if mode == "RATO":
        quantity = 1
    else:
        try:
            quantity = int(str(quantity).strip())
        except ValueError:
            return None, "La cantidad de días debe ser un número entero."

        if quantity < 1 or quantity > 4:
            return None, "La cantidad debe estar entre 1 y 4 días."

    price = TARIFAS[vehicleType][mode]

    charge = {
        "cantidad": quantity,
        "precio": price,
        "total": price * quantity
    }

    return charge, None


def obtenerSiguiente():
    if not pendientes:
        return None

    return pendientes[0]


def retirarSiguiente(ticket):
    current = obtenerSiguiente()

    if current is None:
        return "No hay vehículos pendientes de atención."

    if ticket != current["webToken"]:
        return "La fila cambió. Revisá el siguiente vehículo."

    pendientes.popleft()
    return None


def atenderSiguiente(quantity, ticket, confirmed=True):
    global cabeza

    current = obtenerSiguiente()

    if current is None:
        return None, "No hay vehículos pendientes de atención."

    if ticket != current["webToken"]:
        return None, "La fila cambió. Revisá el siguiente vehículo."

    if not confirmed:
        return None, None

    charge, error = calcularCobro(
        current["tipo"], current["modalidad"], quantity
    )

    if error is not None:
        return None, error

    node = {
        "identificador": current["identificador"],
        "tipo": current["tipo"],
        "modalidad": current["modalidad"],
        "cantidad": charge["cantidad"],
        "precio": charge["precio"],
        "total": charge["total"],
        "date": date.today().isoformat(),
        "siguiente": None
    }

    if cabeza is None:
        cabeza = node
    else:
        last = cabeza

        while last["siguiente"] is not None:
            last = last["siguiente"]

        last["siguiente"] = node

    pendientes.popleft()
    return node, None


def consultarPendientes():
    return list(pendientes)


def consultarCobros():
    records = []
    total = 0
    current = cabeza

    while current is not None:
        records.append(current)
        total += current["total"]
        current = current["siguiente"]

    return records, total


def mostrar_cobros():
    records, total = consultarCobros()

    if not records:
        print("No hay cobros de parqueo registrados.")
        return

    for record in records:
        print(f"{record['identificador']} | "f"{record['tipo']} | {record['modalidad']}" )

        if record["modalidad"] == "DIA":
            print(f"Días: {record['cantidad']}")

        print(f"Precio unitario: C$ {record['precio']}")
        print(f"Total: C$ {record['total']}")

    print(f"Total recibido: C$ {total}")


def solicitarOpcion(message, lower, upper):
    while True:
        try:
            option = int(input(message))

            if lower <= option <= upper:
                return option

            print(f"Seleccione una opción del {lower} al {upper}.")

        except ValueError:
            print("Debe ingresar un número entero.")


def seleccionar_servicio():
    while True:
        print("\n--- SERVICIOS DE PARQUEO ---")
        print("1. Parqueo de moto")
        print("2. Parqueo de bicicleta")
        print("3. Parqueo de carro")
        print("4. Atender siguiente vehículo")
        print("5. Mostrar vehículos pendientes")
        print("6. Volver")
        print("7. Retirar siguiente vehículo sin cobrar")

        option = solicitarOpcion("Seleccione una opción: ", 1, 7)

        if option == 6:
            return

        elif option in (1, 2, 3):
            vehicleType = {1: "MOTO", 2: "BICICLETA", 3: "CARRO"}[option]

            print("1. Por un rato\n2. Por día\n3. Volver")
            modeOption = solicitarOpcion("Seleccione una modalidad: ", 1, 3)

            if modeOption == 3:
                continue

            mode = "RATO" if modeOption == 1 else "DIA"
            label = "Placa del vehículo: "

            if vehicleType == "BICICLETA":
                label = (
                    "Color de la bicicleta: "
                    if mode == "RATO"
                    else "Cédula de identidad: "
                )

            error = registrarPendiente(vehicleType, mode, input(label))
            print(error if error else "Vehículo agregado a la fila.")

        elif option == 4:
            current = obtenerSiguiente()

            if current is None:
                print("No hay vehículos pendientes.")
                continue

            print( f"Vehículo: {current['tipo']} | "f"{current['identificador']} | {current['modalidad']}")

            quantity = 1

            if current["modalidad"] == "DIA":
                quantity = solicitarOpcion("Cantidad de días (1 a 4): ", 1, 4)

            charge, error = calcularCobro(
                current["tipo"], current["modalidad"], quantity
            )

            if error:
                print(error)
                continue

            print(f"Total a pagar: C$ {charge['total']}")
            print("1. Confirmar\n2. Cancelar")

            confirmed = solicitarOpcion("Seleccione una opción: ", 1, 2) == 1

            record, error = atenderSiguiente(
                quantity, current["webToken"], confirmed
            )

            if error:
                print(error)
            elif record is None:
                print("Cobro cancelado. El vehículo permanece pendiente.")
            else:
                print("Vehículo atendido y cobro registrado.")

        elif option == 5:
            records = consultarPendientes()

            if not records:
                print("No hay vehículos pendientes.")

            for position, record in enumerate(records, 1):
                print(
                    f"{position}. {record['identificador']} | "
                    f"{record['tipo']} | {record['modalidad']}"
                )

        elif option == 7:
            current = obtenerSiguiente()

            if current is None:
                print("No hay vehículos pendientes.")
                continue

            print(f"Vehículo que se retirará: {current['identificador']}")
            print("1. Confirmar retiro\n2. Cancelar")

            if solicitarOpcion("Seleccione una opción: ", 1, 2) == 1:
                error = retirarSiguiente(current["webToken"])
                print(error if error else "Vehículo retirado sin cobrar.")