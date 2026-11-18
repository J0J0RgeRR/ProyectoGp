
from collections import deque

# Creamos los nodos donde se guardan los cobros
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


# Aquí guardamos el inicio de la lista de cobros
cabeza = None

# Usamos deque para guardar los vehículos que esperan ser atendidos
pendientes = deque()


# Agregamos un nuevo cobro al final de la lista enlazada
def agregar_cobro(nuevo_nodo):
    global cabeza

    if cabeza is None:
        cabeza = nuevo_nodo

    else:
        actual = cabeza

        while actual["siguiente"] is not None:
            actual = actual["siguiente"]

        actual["siguiente"] = nuevo_nodo


# Creamos el registro de cada vehículo que queda pendiente
def crear_nodo_pendiente(identificador, tipo, modalidad):
    nuevo_nodo = {
        "identificador": identificador,
        "tipo": tipo,
        "modalidad": modalidad
    }

    return nuevo_nodo


# Agregamos los vehículos al final de la cola
def agregar_pendiente(nuevo_nodo):
    pendientes.append(nuevo_nodo)


# Consultamos todos los cobros que se han realizado
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


# Mostramos los vehículos que todavía están esperando
def mostrar_pendientes():

    if not pendientes:
        print("\nNo hay vehículos pendientes de atención.")
        return

    print("\n========== VEHÍCULOS PENDIENTES ==========")

    posicion = 1

    for actual in pendientes:

        print("\nPosición:", posicion)
        print("Identificación:", actual["identificador"])
        print("Vehículo:", actual["tipo"])
        print("Modalidad:", actual["modalidad"])

        posicion += 1


# Le preguntamos al usuario qué modalidad de parqueo necesita
def seleccionar_modalidad(tipo):
    while True:

        print(f"\n========== PARQUEO DE {tipo} ==========")
        print("1. Parqueo por un rato")
        print("2. Parqueo por día")
        print("3. Volver")

        try:
            opcion = int(input("Seleccione una modalidad: "))

            if opcion == 1:
                registrar_pendiente(tipo, "RATO")

            elif opcion == 2:
                registrar_pendiente(tipo, "DIA")

            elif opcion == 3:
                return

            else:
                print("Seleccione una opción del 1 al 3.")

        except ValueError:
            print("Error: debe ingresar un número entero. Intente nuevamente.")


# Pedimos el dato que identifica a cada vehículo

def solicitar_identificador(tipo, modalidad):
    while True:

        if tipo == "MOTO" or tipo == "CARRO":
            identificador = input("Ingrese la placa del vehículo: ")

        elif tipo == "BICICLETA" and modalidad == "RATO":
            identificador = input("Ingrese el color de la bicicleta: ")

        else:
            identificador = input("Ingrese la cédula de identidad: ")

        identificador = identificador.strip().upper()

        if identificador == "":
            print("Error: el campo no puede estar vacío. Intente nuevamente.")

        elif tipo == "BICICLETA" and modalidad == "RATO":
            if identificador.replace(" ", "").isalpha():
                return identificador

            print("Error: el color solo debe contener letras. Intente nuevamente.")

        else:
            return identificador



# Definimos los precios según el vehículo y la modalidad
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


# Calculamos cuánto debe pagar el vehículo
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


# Atendemos el primer vehículo que llegó a la cola
def atender_siguiente():

    if not pendientes:
        print("\nNo hay vehículos pendientes de atención.")
        return

    actual = pendientes[0]

    print("\n========== ATENCIÓN DE VEHÍCULO ==========")
    print("Identificación:", actual["identificador"])
    print("Vehículo:", actual["tipo"])
    print("Modalidad:", actual["modalidad"])

    cantidad, precio, total = calcular_cobro(
        actual["tipo"],
        actual["modalidad"]
    )

    print("\n========== RESUMEN DEL COBRO ==========")
    print("Identificación:", actual["identificador"])
    print("Vehículo:", actual["tipo"])
    print("Modalidad:", actual["modalidad"])

    if actual["modalidad"] == "DIA":
        print("Cantidad de días:", cantidad)

    print("Precio unitario: C$", precio)
    print("Total a pagar: C$", total)

    while True:

        confirmacion = input(
            "\n¿Desea confirmar el cobro? (S/N): "
        ).strip().upper()

        if confirmacion == "S":

            nuevo_nodo = crear_nodo(
                actual["identificador"],
                actual["tipo"],
                actual["modalidad"],
                cantidad,
                precio,
                total
            )

            agregar_cobro(nuevo_nodo)

            # Quitamos de la cola al vehículo que ya fue atendido
            pendientes.popleft()

            print("\n¡Vehículo atendido y cobro registrado!")
            break

        elif confirmacion == "N":

            print("\nCobro cancelado. El vehículo permanece pendiente.")
            break

        else:
            print("Error: ingrese S para confirmar o N para cancelar.")


# Registramos el vehículo para que espere su turno
def registrar_pendiente(tipo, modalidad):

    identificador = solicitar_identificador(tipo, modalidad)

    nuevo_nodo = crear_nodo_pendiente(
        identificador,
        tipo,
        modalidad
    )

    agregar_pendiente(nuevo_nodo)

    print("\n¡Vehículo agregado a la cola de atención!")
    print("Identificación:", identificador)
    print("Vehículo:", tipo)
    print("Modalidad:", modalidad)
    print("Estado: Pendiente de atención.")


# Menú donde se seleccionan los servicios de parqueo
def seleccionar_servicio():
    while True:

        print("\n========== SERVICIOS DE PARQUEO ==========")
        print("1. Parqueo de moto")
        print("2. Parqueo de bicicleta")
        print("3. Parqueo de carro")
        print("4. Atender siguiente vehículo")
        print("5. Mostrar vehículos pendientes")
        print("6. Volver")

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                seleccionar_modalidad("MOTO")

            elif opcion == 2:
                seleccionar_modalidad("BICICLETA")

            elif opcion == 3:
                seleccionar_modalidad("CARRO")

            elif opcion == 4:
                atender_siguiente()

            elif opcion == 5:
                mostrar_pendientes()

            elif opcion == 6:
                return

            else:
                print("Seleccione una opción del 1 al 6.")

        except ValueError:
            print("Error: debe ingresar un número entero. Intente nuevamente.")
