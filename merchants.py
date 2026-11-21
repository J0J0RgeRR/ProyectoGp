from datetime import date

import expenses

root = None
payments = []


def crearNodo(local, name, business, phone, rent):
    node = {
        "local": local,
        "name": name,
        "business": business,
        "phone": phone,
        "rent": rent,
        "balance": 0.0,
        "chargedMonth": "",
        "left": None,
        "right": None
    }

    return node


def validarDatos(name, business, phone, rent):
    name = name.strip()
    business = business.strip()
    phone = phone.strip()

    if name == "" or business == "" or phone == "":
        return None, "Completá el nombre, el giro y el teléfono."

    digits = 0

    for character in phone:
        if character.isdigit():
            digits += 1
        elif character not in "+- ":
            return None, "El teléfono solo puede tener números, espacios, + o -."

    if digits < 8:
        return None, "El teléfono debe tener al menos 8 dígitos."

    amount, error = expenses.validarMonto(rent)

    if error is not None:
        return None, error

    if amount <= 0:
        return None, "La renta mensual debe ser mayor que cero."

    data = {
        "name": name,
        "business": business,
        "phone": phone,
        "rent": amount
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

        for field in ("local", "name", "business", "phone", "rent", "balance", "chargedMonth"):
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


def registrarComerciante(local, name, business, phone, rent):
    global root

    local = normalizarLocal(local)

    if local is None:
        return "El código del local solo puede tener letras, números y guiones."

    if buscarComerciante(local) is not None:
        return "Ese local ya tiene un comerciante registrado."

    data, error = validarDatos(name, business, phone, rent)

    if error is not None:
        return error

    node = crearNodo(local, data["name"], data["business"], data["phone"], data["rent"])
    root = insertarNodo(root, node)

    return None


def modificarComerciante(local, name, business, phone, rent):
    node = buscarComerciante(local)

    if node is None:
        return "El local no existe."

    data, error = validarDatos(name, business, phone, rent)

    if error is not None:
        return error

    node["name"] = data["name"]
    node["business"] = data["business"]
    node["phone"] = data["phone"]
    node["rent"] = data["rent"]

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
            total += node["balance"]

    total = round(total, 2)

    return debtors, total


def generarCobroMensual():
    records = consultarComerciantes()

    if len(records) == 0:
        return 0, "No hay comerciantes registrados."

    month = date.today().strftime("%Y-%m")
    charged = 0

    for node in records:
        if node["chargedMonth"] != month:
            node["balance"] = round(node["balance"] + node["rent"], 2)
            node["chargedMonth"] = month
            charged += 1

    if charged == 0:
        return 0, "El cobro de este mes ya fue generado."

    return charged, None


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
        "amount": amount
    }

    payments.append(payment)

    return payment, None


def consultarPagos():
    total = 0

    for payment in payments:
        total += payment["amount"]

    total = round(total, 2)

    return payments, total


def consultarAltura():
    return calcularAltura(root)


def calcularIngresosEsperados():
    total = 0

    for node in consultarComerciantes():
        total += node["rent"]

    total = round(total, 2)

    return total