from datetime import date, timedelta

import expenses

root = None
payments = []


def crearNodo(local, name, business, phone, rent, frequency):
    node = {
        "local": local,
        "name": name,
        "business": business,
        "phone": phone,
        "rent": rent,
        "frequency": frequency,
        "balance": 0.0,
        "chargedPeriods": [],
        "left": None,
        "right": None
    }

    return node


def validarDatos(name, business, phone, rent, frequency):
    name = name.strip()
    business = business.strip()
    phone = phone.strip()
    frequency = frequency.strip().lower()

    if name == "" or business == "" or phone == "":
        return None, "Completá el nombre, el giro y el teléfono."

    digits = 0

    for character in phone:
        if character.isdigit():
            digits = digits + 1
        elif character not in "+- ":
            return None, "El teléfono solo puede tener números, espacios, + o -."

    if digits < 8:
        return None, "El teléfono debe tener al menos 8 dígitos."

    if frequency != "diario" and frequency != "semanal":
        return None, "Seleccioná cobro diario o semanal."

    amount, error = expenses.validarMonto(rent)

    if error is not None:
        return None, error

    if amount <= 0:
        return None, "El monto del cobro debe ser mayor que cero."

    data = {
        "name": name,
        "business": business,
        "phone": phone,
        "rent": amount,
        "frequency": frequency
    }

    return data, None


def normalizarLocal(local):
    local = local.strip().upper()

    if local == "" or not local.replace("-", "").isalnum():
        return None

    return local


def insertarNodo(current, node):
    if current is None:
        return node

    if node["local"] < current["local"]:
        current["left"] = insertarNodo(current["left"], node)
    else:
        current["right"] = insertarNodo(current["right"], node)

    return current


def buscarComerciante(local):
    local = local.strip().upper()
    current = root

    while current is not None:
        if local == current["local"]:
            return current
        elif local < current["local"]:
            current = current["left"]
        else:
            current = current["right"]

    return None


def eliminarNodo(current, local):
    if current is None:
        return None

    if local < current["local"]:
        current["left"] = eliminarNodo(current["left"], local)
    elif local > current["local"]:
        current["right"] = eliminarNodo(current["right"], local)
    else:
        if current["left"] is None:
            return current["right"]

        if current["right"] is None:
            return current["left"]

        successor = current["right"]

        while successor["left"] is not None:
            successor = successor["left"]

        for field in (
            "local", "name", "business", "phone", "rent",
            "frequency", "balance", "chargedPeriods"
        ):
            current[field] = successor[field]

        current["right"] = eliminarNodo(current["right"], successor["local"])

    return current


def recorrerInorden(current, records):
    if current is None:
        return

    recorrerInorden(current["left"], records)
    records.append(current)
    recorrerInorden(current["right"], records)


def calcularAltura(current):
    if current is None:
        return 0

    left = calcularAltura(current["left"])
    right = calcularAltura(current["right"])

    return 1 + max(left, right)


def registrarComerciante(local, name, business, phone, rent, frequency):
    global root

    local = normalizarLocal(local)

    if local is None:
        return "El código del local solo puede tener letras, números y guiones."

    if buscarComerciante(local) is not None:
        return "Ese local ya tiene un comerciante registrado."

    data, error = validarDatos(name, business, phone, rent, frequency)

    if error is not None:
        return error

    node = crearNodo(local, data["name"], data["business"], data["phone"], data["rent"], data["frequency"])
    root = insertarNodo(root, node)

    return None


def modificarComerciante(local, name, business, phone, rent, frequency):
    node = buscarComerciante(local)

    if node is None:
        return "El local no existe."

    data, error = validarDatos(name, business, phone, rent, frequency)

    if error is not None:
        return error

    if data["frequency"] != node["frequency"] and len(node["chargedPeriods"]) > 0:
        return "No se puede cambiar la modalidad de un comerciante que ya tiene cobros registrados."

    node["name"] = data["name"]
    node["business"] = data["business"]
    node["phone"] = data["phone"]
    node["rent"] = data["rent"]

    node["frequency"] = data["frequency"]

    return None


def eliminarComerciante(local):
    global root

    node = buscarComerciante(local)

    if node is None:
        return "El local no existe."

    if node["balance"] > 0:
        return "No se puede eliminar un comerciante con saldo pendiente."

    root = eliminarNodo(root, node["local"])

    return None


def consultarComerciantes():
    records = []
    recorrerInorden(root, records)

    return records


def consultarMorosos():
    debtors = []
    total = 0

    for node in consultarComerciantes():
        if node["balance"] > 0:
            debtors.append(node)
            total = total + node["balance"]

    total = round(total, 2)

    return debtors, total


def obtenerPeriodo(frequency):
    today = date.today()

    if frequency == "diario":
        period = today.isoformat()
    else:
        monday = today - timedelta(days=today.weekday())
        period = monday.isoformat()

    return period


def generarCobro(local):
    node = buscarComerciante(local)

    if node is None:
        return "El local no existe."

    period = obtenerPeriodo(node["frequency"])

    if period in node["chargedPeriods"]:
        return "El cobro de este período ya fue generado."

    node["balance"] = round(node["balance"] + node["rent"], 2)
    node["chargedPeriods"].append(period)

    return None


def registrarPago(local, value):
    node = buscarComerciante(local)

    if node is None:
        return None, "El local no existe."

    amount, error = expenses.validarMonto(value)

    if error is not None:
        return None, error

    if amount <= 0:
        return None, "El monto mínimo es C$0.01."

    if node["balance"] <= 0:
        return None, "Este comerciante no tiene saldo pendiente."

    if amount > node["balance"]:
        return None, "El pago supera el saldo pendiente."

    node["balance"] = round(node["balance"] - amount, 2)

    payment = {
        "local": node["local"],
        "name": node["name"],
        "amount": amount,
        "date": date.today().isoformat(),
        "frequency": node["frequency"]
    }

    payments.append(payment)

    return payment, None


def consultarPagos():
    total = 0

    for payment in payments:
        total = total + payment["amount"]

    total = round(total, 2)

    return payments, total


def consultarAltura():
    height = calcularAltura(root)

    return height