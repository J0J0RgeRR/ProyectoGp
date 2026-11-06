
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
