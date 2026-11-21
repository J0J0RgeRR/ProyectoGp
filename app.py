from secrets import token_hex
from flask import Flask, redirect, render_template, request, session, url_for

import bathrooms
import cash
import expenses
import merchants
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
    records, parkingTotal = parking.consultarCobros()
    merchantPayments, merchantTotal = merchants.consultarPagos()
    summary = cash.consultarResumen(currentCash, sales, parkingTotal, merchantTotal, expenseRecords)

    return summary


def validarCaja():
    token = request.form.get("cashToken", "")
    error = cash.validarCaja(currentCash, token)

    return error


@app.context_processor
def compartirCaja():
    cashOpen = False
    cashToken = ""

    if currentCash is not None:
        cashOpen = True
        cashToken = currentCash["token"]

    data = {
        "cashOpen": cashOpen,
        "cashToken": cashToken
    }

    return data


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
        "index.html", role=role, page="inicio",
        error=error, username=username
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
        error = validarCaja()

        if error is None:
            option = request.form.get("service", "")
            stock, saved, result = bathrooms.guardarCobro(stock, sales, option)

            if saved:
                session["bathroomMessage"] = result
                return redirect(url_for("cobrarBaños"))
            else:
                error = result

    total = bathrooms.calcularTotalCobros(sales)

    return render_template(
        "index.html", role=role, page="baños",
        error=error, message=message, sales=sales, total=total
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
                session["inventoryMessage"] = f"Se agregaron {rolls} rollos: {rolls * 18} unidades."

                return redirect(url_for("consultarInventario"))

        except ValueError:
            error = "Ingresá una cantidad entera de rollos."

    return render_template(
        "index.html", role=role, page="inventario",
        stock=stock, error=error, message=message
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
        "index.html", role=role, page="rutas",
        zones=rutas.grafo, origin=origin,
        destination=destination, path=path, error=error
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
            vehicleType = request.form.get("vehicleType", "")
            mode = request.form.get("mode", "")
            identifier = request.form.get("identifier", "")

            error = parking.registrarPendiente(vehicleType, mode, identifier)
            message = "Vehículo agregado a la fila de atención."

        elif action == "retirar":
            ticket = request.form.get("ticket", "")

            error = parking.retirarSiguiente(ticket)
            message = "Vehículo retirado de la fila sin cobrar."

        elif action == "atender":
            error = validarCaja()

            if error is None:
                days = request.form.get("days", "1")
                ticket = request.form.get("ticket", "")

                record, error = parking.atenderSiguiente(days, ticket, True)

                if error is None:
                    message = f"Cobro confirmado: C${record['total']:.2f}"

        else:
            error = "Seleccioná una operación válida."

        if error is None:
            session["parkingMessage"] = message
            return redirect(url_for("gestionarParqueo"))

        message = None

    first = parking.obtenerSiguiente()
    unitPrice = 0

    if first is not None:
        charge, chargeError = parking.calcularCobro(first["tipo"], first["modalidad"], 1)

        if chargeError is None:
            unitPrice = charge["precio"]

    waiting = parking.consultarPendientes()
    history, totalParking = parking.consultarCobros()

    return render_template(
        "index.html", role=role, page="parqueo",
        error=error, message=message, waiting=waiting,
        first=first, unitPrice=unitPrice,
        history=history, totalParking=totalParking
    )


@app.route("/comerciantes", methods=["GET", "POST"])
def gestionarComerciantes():
    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    error = None
    message = session.pop("merchantMessage", None)

    if request.method == "POST":
        action = request.form.get("action", "")
        local = request.form.get("local", "")

        if action == "pagar":
            error = validarCaja()

            if error is None:
                amount = request.form.get("amount", "")

                payment, error = merchants.registrarPago(local, amount)

                if error is None:
                    message = f"Pago confirmado: C${payment['amount']:.2f}"

        elif role != "administrador":
            return "Solo el administrador puede gestionar comerciantes.", 403

        elif action == "registrar":
            name = request.form.get("name", "")
            business = request.form.get("business", "")
            phone = request.form.get("phone", "")
            rent = request.form.get("rent", "")

            error = merchants.registrarComerciante(local, name, business, phone, rent)
            message = "Comerciante registrado correctamente."

        elif action == "modificar":
            name = request.form.get("name", "")
            business = request.form.get("business", "")
            phone = request.form.get("phone", "")
            rent = request.form.get("rent", "")

            error = merchants.modificarComerciante(local, name, business, phone, rent)
            message = "Comerciante actualizado correctamente."

        elif action == "eliminar":
            error = merchants.eliminarComerciante(local)
            message = "Comerciante eliminado del árbol."

        elif action == "cobroMensual":
            charged, error = merchants.generarCobroMensual()
            message = f"Cobro mensual generado para {charged} comerciantes."

        else:
            error = "Seleccioná una operación válida."

        if error is None:
            session["merchantMessage"] = message
            return redirect(url_for("gestionarComerciantes"))

        message = None

    search = request.args.get("search", "").strip()
    found = None

    if search != "":
        found = merchants.buscarComerciante(search)

        if found is None:
            error = "No hay ningún comerciante en ese local."

    merchantList = merchants.consultarComerciantes()
    debtors, totalDebt = merchants.consultarMorosos()
    merchantPayments, totalPayments = merchants.consultarPagos()

    return render_template(
        "index.html", role=role, page="comerciantes",
        error=error, message=message, merchantList=merchantList,
        debtors=debtors, totalDebt=totalDebt,
        merchantPayments=merchantPayments, totalPayments=totalPayments,
        expectedIncome=merchants.calcularIngresosEsperados(),
        treeHeight=merchants.consultarAltura(),
        search=search, found=found
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
            initialAmount = request.form.get("initialAmount", "")
            records, parkingTotal = parking.consultarCobros()
            merchantPayments, merchantTotal = merchants.consultarPagos()
            token = token_hex(8)

            currentCash, error = cash.iniciarCaja(currentCash, initialAmount, sales, parkingTotal, merchantTotal, expenseRecords, token)
            message = "Caja abierta correctamente."

        elif action in ("gasto", "cerrar"):
            error = validarCaja()

            if error is None:
                summary = obtenerResumen()

                if action == "gasto":
                    amount = request.form.get("amount", "")
                    description = request.form.get("description", "")
                    balance = summary["balance"]

                    saved, result = expenses.guardarGasto(expenseRecords, amount, description, balance)

                    if saved:
                        message = result
                    else:
                        error = result

                else:
                    countedCash = request.form.get("countedCash", "")

                    currentCash, error = cash.finalizarCaja(currentCash, cashClosings, countedCash, summary)
                    message = "Caja cerrada. Revisá el resultado del cierre."

        else:
            error = "Seleccioná una operación válida."

        if error is None:
            session["expenseMessage"] = message
            return redirect(url_for("gestionarGastos"))

        message = None

    currentExpenses = []

    if currentCash is not None:
        currentExpenses = expenseRecords[currentCash["expenseStart"]:]

    summary = obtenerResumen()

    return render_template(
        "index.html", role=role, page="gastos",
        error=error, message=message, summary=summary,
        currentExpenses=currentExpenses, cashClosings=cashClosings
    )


@app.post("/cerrar-sesion")
def cerrarSesion():
    session.clear()

    return redirect(url_for("inicio"))


if __name__ == "__main__":
    app.run()