from secrets import token_hex

from flask import Flask, redirect, render_template, request, session, url_for

import bathrooms
import cash
import expenses
import paper
import parking
import rutas
import users


app = Flask(__name__)
app.secret_key = token_hex(32)

stock = 0
sales = []
expenseRecords = []

currentCash = None
cashClosings = []


def obtenerResumen():
    if currentCash is None:
        return None

    bathroomIncome = (
        bathrooms.calcularTotalCobros(sales)
        - currentCash["bathroomStart"]
    )

    records, parkingTotal = parking.consultarCobros()
    parkingIncome = parkingTotal - currentCash["parkingStart"]

    totalExpenses = 0

    for expense in expenseRecords[currentCash["expenseStart"]:]:
        totalExpenses += expense["amount"]

    return cash.resumirCaja(
        currentCash["initialAmount"],
        bathroomIncome,
        parkingIncome,
        0,
        round(totalExpenses, 2)
    )


def validarCaja():
    if currentCash is None:
        return "Primero abrí la caja desde Caja y gastos."

    if request.form.get("cashToken") != currentCash["token"]:
        return "La caja cambió. Recargá la página e intentá nuevamente."

    return None


@app.context_processor
def compartirCaja():
    return {
        "cashOpen": currentCash is not None,
        "cashToken": currentCash["token"] if currentCash else ""
    }

@app.route("/", methods=["GET", "POST"])
def inicio():
    role = session.get("role")
    error = None
    username = ""

    if role is None and request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if username == "" or password.strip() == "":
            error = "Completá el usuario y la contraseña."
        else:
            role = users.validarUsuario(username, password)

            if role is None:
                error = "Usuario o contraseña incorrectos."
            else:
                session["role"] = role
                return redirect(url_for("inicio"))

    return render_template(
        "index.html",
        role=role,
        page="inicio",
        error=error,
        username=username
    )

@app.route("/baños", methods=["GET", "POST"])
def cobrarBaños():
    global stock

    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    error = None
    message = session.pop("bathroomMessage", None)

    if request.method == "POST":
        try:
            option = int(request.form.get("service", ""))
        except ValueError:
            option = 0

        error = validarCaja()

        if error is not None:
            pass
        elif option not in (1, 2, 3):
            error = "Seleccioná un servicio válido."
        else:
            price = bathrooms.calcularPrecio(option)

            if option == 1:
                service = "Sanitario: 1 unidad"
                units = 1
            elif option == 2:
                service = "Sanitario: 2 unidades"
                units = 2
            else:
                service = "Urinario para varones"
                units = 0

            if stock < units:
                error = "No hay suficiente papel para registrar este servicio."
            else:
                stock = paper.descontarPapel(stock, units)

                sales.append({
                    "service": service,
                    "price": price
                })

                session["bathroomMessage"] = (
                    f"Cobro confirmado: C${price:.2f}"
                )

                return redirect(url_for("cobrarBaños"))

    return render_template(
        "index.html",
        role=role,
        page="baños",
        error=error,
        message=message,
        sales=sales,
        total=bathrooms.calcularTotalCobros(sales)
    )


@app.route("/inventario", methods=["GET", "POST"])
def consultarInventario():
    global stock

    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    error = None
    message = session.pop("inventoryMessage", None)

    if request.method == "POST":
        if role != "administrador":
            return "Solo el administrador puede ingresar rollos.", 403

        try:
            rolls = int(request.form.get("rolls", ""))

            if rolls <= 0:
                error = "La cantidad de rollos debe ser mayor que cero."
            else:
                stock = paper.agregarRollos(stock, rolls)

                session["inventoryMessage"] = (
                    f"Se agregaron {rolls} rollos: {rolls * 18} unidades."
                )

                return redirect(url_for("consultarInventario"))

        except ValueError:
            error = "Ingresá una cantidad entera de rollos."

    return render_template(
        "index.html",
        role=role,
        page="inventario",
        stock=stock,
        error=error,
        message=message
    )


@app.get("/rutas")
def consultarRutas():
    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    origin = request.args.get("origin", "")
    destination = request.args.get("destination", "")
    path = None
    error = None

    if "origin" in request.args or "destination" in request.args:
        if origin not in rutas.grafo or destination not in rutas.grafo:
            error = "Seleccioná una zona válida de origen y de destino."
        else:
            path = rutas.buscarRuta(origin, destination)

            if path is None:
                error = "No hay un recorrido entre esas zonas."

    return render_template(
        "index.html",
        role=role,
        page="rutas",
        zones=rutas.grafo,
        origin=origin,
        destination=destination,
        path=path,
        error=error
    )


@app.route("/parqueo", methods=["GET", "POST"])
def gestionarParqueo():
    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    error = None
    message = session.pop("parkingMessage", None)

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "registrar":
            error = parking.registrarPendiente(
                request.form.get("vehicleType", ""),
                request.form.get("mode", ""),
                request.form.get("identifier", "")
            )

            message = "Vehículo agregado a la fila de atención."

        elif action == "retirar":
            error = parking.retirarSiguiente(
                request.form.get("ticket", "")
            )

            message = "Vehículo retirado de la fila sin cobrar."

        elif action == "atender":
            error = validarCaja()

            if error is None:
                record, error = parking.atenderSiguiente(
                    request.form.get("days", "1"),
                    request.form.get("ticket", ""),
                    True
                )

                if error is None:
                    message = (
                        f"Cobro confirmado: C${record['total']:.2f}"
                    )
        else:
            error = "Seleccioná una operación válida."

        if error is None:
            session["parkingMessage"] = message
            return redirect(url_for("gestionarParqueo"))

        message = None

    first = parking.obtenerSiguiente()
    unitPrice = 0

    if first is not None:
        charge, chargeError = parking.calcularCobro(
            first["tipo"],
            first["modalidad"],
            1
        )

        if chargeError is None:
            unitPrice = charge["precio"]

    history, totalParking = parking.consultarCobros()

    return render_template(
        "index.html",
        role=role,
        page="parqueo",
        error=error,
        message=message,
        waiting=parking.consultarPendientes(),
        first=first,
        unitPrice=unitPrice,
        history=history,
        totalParking=totalParking
    )


@app.route("/gastos", methods=["GET", "POST"])
def gestionarGastos():
    global currentCash

    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    error = None
    message = session.pop("expenseMessage", None)

    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "abrir":
            if currentCash is not None:
                error = "Ya hay una caja abierta."
            else:
                amount, error = cash.validarMonto(
                    request.form.get("initialAmount", "")
                )

                if error is None:
                    records, parkingTotal = parking.consultarCobros()

                    currentCash = {
                        "initialAmount": amount,
                        "bathroomStart": bathrooms.calcularTotalCobros(sales),
                        "parkingStart": parkingTotal,
                        "expenseStart": len(expenseRecords),
                        "token": token_hex(8)
                    }

                    message = "Caja abierta correctamente."

        elif action in ("gasto", "cerrar"):
            error = validarCaja()

            if error is None:
                summary = obtenerResumen()

                if action == "gasto":
                    amount, error = cash.validarMonto(
                        request.form.get("amount", "")
                    )

                    if error is None:
                        if amount > summary["balance"]:
                            error = (
                                "El gasto supera el saldo disponible en caja."
                            )
                        else:
                            saved, result = expenses.guardarGasto(
                                expenseRecords,
                                amount,
                                request.form.get("description", "")
                            )

                            if saved:
                                message = result
                            else:
                                error = result
                else:
                    countedCash, error = cash.validarMonto(
                        request.form.get("countedCash", "")
                    )

                    if error is None:
                        summary["countedCash"] = countedCash
                        summary["difference"] = cash.calcularDiferencia(
                            summary["balance"],
                            countedCash
                        )

                        cashClosings.append(summary)
                        currentCash = None
                        message = (
                            "Caja cerrada. Revisá el resultado del cierre."
                        )
        else:
            error = "Seleccioná una operación válida."

        if error is None:
            session["expenseMessage"] = message
            return redirect(url_for("gestionarGastos"))

    currentExpenses = []

    if currentCash is not None:
        currentExpenses = expenseRecords[currentCash["expenseStart"]:]

    return render_template(
        "index.html",
        role=role,
        page="gastos",
        error=error,
        message=message,
        summary=obtenerResumen(),
        currentExpenses=currentExpenses,
        cashClosings=cashClosings
    )


@app.post("/cerrar-sesion")
def cerrarSesion():
    session.clear()
    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run()