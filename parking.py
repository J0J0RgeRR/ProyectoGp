
def crear_nodo(identificador, tipo, modalidad, cantidad, precio, total):
    nuevo_nodo = {
        "identificador": identificador,
        "tipo": tipo,
        "modalidad": modalidad,
        "cantidad": cantidad,
        "precio": precio,
        "total": total,
        "siguiente": None
    }

    return nuevo_nodo

cabeza = None


def agregar_cobro(nuevo_nodo):
    global cabeza

    if cabeza is None:
        cabeza = nuevo_nodo

    else:
        actual = cabeza

        while actual["siguiente"] is not None:
            actual = actual["siguiente"]

        actual["siguiente"] = nuevo_nodo

def buscar_rato(identificador, tipo):
    actual = cabeza

    while actual is not None:

        if (actual["identificador"] == identificador
                and actual["tipo"] == tipo
                and actual["modalidad"] == "RATO"):

            return True

        actual = actual["siguiente"]

    return False

def mostrar_cobros():
    actual = cabeza

    if actual is None:
        print("\nNo hay cobros de parqueo registrados.")
        return

    print("\n========== HISTORIAL DE PARQUEO ==========")

    while actual is not None:

        print("\nIdentificación:", actual["identificador"])
        print("Vehículo:", actual["tipo"])
        print("Modalidad:", actual["modalidad"])

        if actual["modalidad"] == "DIA":
            print("Cantidad de días:", actual["cantidad"])

        print("Precio unitario: C$", actual["precio"])
        print("Total: C$", actual["total"])

        actual = actual["siguiente"]


def seleccionar_modalidad(tipo):
    while True:
        print(f"\n========== PARQUEO DE {tipo} ==========")
        print("1. Parqueo por un rato")
        print("2. Parqueo por día")
        print("3. Volver")

        try:
            opcion = int(input("Seleccione una modalidad: "))

            if opcion == 1:
                registrar_cobro(tipo, "RATO")
            elif opcion == 2:
                registrar_cobro(tipo, "DIA")
            elif opcion == 3:
                return
            else:
                print("Seleccione una opción del 1 al 3.")

        except ValueError:
            print("Error: debe ingresar un número entero. Intente nuevamente.")

def solicitar_identificador(tipo, modalidad):
    while True:
        if tipo == "MOTO" or tipo == "CARRO":
            identificador = input("Ingrese la placa del vehículo: ")

        elif tipo == "BICICLETA" and modalidad == "RATO":
            identificador = input("Ingrese el color de la bicicleta: ")

        else:
            identificador = input("Ingrese la cédula de identidad: ")

        identificador = identificador.strip().upper()

        if identificador != "":
            return identificador

        print("Error: el campo no puede estar vacío. Intente nuevamente.")

TARIFAS = {
    "MOTO": {
        "RATO": 20,
        "DIA": 30
    },
    "BICICLETA": {
        "RATO": 10,
        "DIA": 20
    },
    "CARRO": {
        "RATO": 30,
        "DIA": 50
    }
}

def calcular_cobro(tipo, modalidad):
    precio = TARIFAS[tipo][modalidad]

    if modalidad == "RATO":
        cantidad = 1
        total = precio

    else:
        while True:
            try:
                cantidad = int(input("Ingrese la cantidad de días (1 a 4): "))

                if 1 <= cantidad <= 4:
                    break

                print("Error: la cantidad debe estar entre 1 y 4 días.")

            except ValueError:
                print("Error: debe ingresar un número entero. Intente nuevamente.")

        total = precio * cantidad

    return cantidad, precio, total

def registrar_cobro(tipo, modalidad):
    identificador = solicitar_identificador(tipo, modalidad)

    if modalidad == "RATO":
        if buscar_rato(identificador, tipo):
            print("\nEste vehículo ya tiene registrado un parqueo por rato.")
            return

    cantidad, precio, total = calcular_cobro(tipo, modalidad)

    print("\n========== RESUMEN DEL COBRO ==========")
    print("Identificación:", identificador)
    print("Vehículo:", tipo)
    print("Modalidad:", modalidad)

    if modalidad == "DIA":
        print("Cantidad de días:", cantidad)

    print("Precio unitario: C$", precio)
    print("Total a pagar: C$", total)

    while True:
        confirmacion = input(
            "\n¿Desea confirmar el cobro? (S/N): "
        ).strip().upper()

        if confirmacion == "S":
            nuevo_nodo = crear_nodo(
                identificador,
                tipo,
                modalidad,
                cantidad,
                precio,
                total
            )

            agregar_cobro(nuevo_nodo)

            print("\n¡Cobro registrado correctamente!")
            break

        elif confirmacion == "N":
            print("\nRegistro de cobro cancelado.")
            break

        else:
            print("Error: ingrese S para confirmar o N para cancelar.")

def seleccionar_servicio():
    while True:
        print("\n========== SERVICIOS DE PARQUEO ==========")
        print("1. Parqueo de moto")
        print("2. Parqueo de bicicleta")
        print("3. Parqueo de carro")
        print("4. Volver")
        
        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                seleccionar_modalidad("MOTO")

            elif opcion == 2:
                seleccionar_modalidad("BICICLETA")

            elif opcion == 3:
                seleccionar_modalidad("CARRO")

            elif opcion == 4:
                return

            else:
                print("Seleccione una opción del 1 al 4.")

        except ValueError:
            print("Error: debe ingresar un número entero. Intente nuevamente.")
