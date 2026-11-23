from secrets import token_hex
from datetime import date
from copy import deepcopy
from flask import Flask, redirect, render_template, request, session, url_for, g, jsonify

import bathrooms
import cash
import expenses
import files
import reports
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


def obtenerDatos():
    history, total = parking.consultarCobros()
    parkingRecords = []

    for record in history:
        item = record.copy()
        item.pop("siguiente", None)
        parkingRecords.append(item)

    data = {
        "stock": stock,
        "sales": sales,
        "expenseRecords": expenseRecords,
        "currentCash": currentCash,
        "cashClosings": cashClosings,
        "parkingWaiting": parking.consultarPendientes(),
        "parkingRecords": parkingRecords,
        "nextTicket": parking.nextTicket,
        "merchantRoot": merchants.root,
        "merchantPayments": merchants.payments
    }

    return data


def aplicarDatos(data):
    global stock, sales, expenseRecords, currentCash, cashClosings

    stock = data["stock"]
    sales = data["sales"]
    expenseRecords = data["expenseRecords"]
    currentCash = data["currentCash"]
    cashClosings = data["cashClosings"]
    merchants.root = data["merchantRoot"]
    merchants.payments = data["merchantPayments"]
    parking.nextTicket = data["nextTicket"]

    parking.pendientes.clear()
    parking.pendientes.extend(data["parkingWaiting"])

    parking.cabeza = None
    last = None

    for record in data["parkingRecords"]:
        record["siguiente"] = None

        if last is None:
            parking.cabeza = record
        else:
            last["siguiente"] = record

        last = record


def cargarEstado():
    data, error = files.cargarDatos("sistema.json")

    if error is not None:
        raise RuntimeError(error)

    if data is not None:
        if not isinstance(data, dict):
            raise RuntimeError("El archivo sistema.json no tiene el formato esperado.")

        requiredFields = obtenerDatos()

        for field in requiredFields:
            if field not in data:
                raise RuntimeError("Falta el campo " + field + " en sistema.json.")

        aplicarDatos(data)


@app.before_request
def prepararOperacion():
    if request.method == "POST" and request.endpoint in ("cobrarBaños", "consultarInventario", "gestionarParqueo", "gestionarComerciantes", "gestionarGastos"):
        g.previousData = deepcopy(obtenerDatos())


@app.after_request
def guardarOperacion(response):
    if hasattr(g, "previousData"):
        if response.status_code == 302 and session.get("role") in ("administrador", "trabajador"):
            error = files.guardarDatos("sistema.json", obtenerDatos())

            if error is not None:
                aplicarDatos(g.previousData)

                session.pop("bathroomMessage", None)
                session.pop("inventoryMessage", None)
                session.pop("parkingMessage", None)
                session.pop("merchantMessage", None)
                session.pop("expenseMessage", None)

                return app.make_response((error + " La operación fue cancelada. Intentá nuevamente.", 500))
        else:
            aplicarDatos(g.previousData)

    return response


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

        elif action == "generar":
            error = merchants.generarCobro(local)
            message = "Cobro generado para el período actual."

        elif role != "administrador":
            return "Solo el administrador puede gestionar comerciantes.", 403

        elif action == "registrar":
            name = request.form.get("name", "")
            business = request.form.get("business", "")
            phone = request.form.get("phone", "")
            rent = request.form.get("rent", "")
            frequency = request.form.get("frequency", "")

            error = merchants.registrarComerciante(local, name, business, phone, rent, frequency)
            message = "Comerciante registrado correctamente."

        elif action == "modificar":
            name = request.form.get("name", "")
            business = request.form.get("business", "")
            phone = request.form.get("phone", "")
            rent = request.form.get("rent", "")
            frequency = request.form.get("frequency", "")

            error = merchants.modificarComerciante(local, name, business, phone, rent, frequency)
            message = "Comerciante actualizado correctamente."

        elif action == "eliminar":
            error = merchants.eliminarComerciante(local)
            message = "Comerciante eliminado del árbol."

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

                    summary["date"] = date.today().isoformat()

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


@app.get("/reportes")
def consultarReportes():
    role = session.get("role")

    if role not in ("administrador", "trabajador"):
        return redirect(url_for("inicio"))

    today = date.today().isoformat()
    reportType = request.args.get("type", "diario")
    referenceDate = request.args.get("date", today)

    if role == "trabajador" and (reportType != "diario" or referenceDate != today):
        return "Solo podés consultar el reporte del día actual.", 403

    parkingRecords, total = parking.consultarCobros()
    merchantPayments, merchantTotal = merchants.consultarPagos()

    report, error = reports.generarReporte(reportType, referenceDate, sales, parkingRecords, merchantPayments, expenseRecords)

    if error is None and request.args.get("download") == "1":
        fileName, error = reports.guardarReporte(report)

        if error is None:
            response = jsonify(report)

            response.headers["Content-Disposition"] = 'attachment; filename="' + fileName.split("/")[-1] + '"'

            return response

    return render_template(
        "index.html", role=role, page="reportes", report=report,
        error=error, reportType=reportType, referenceDate=referenceDate
    )


@app.post("/cerrar-sesion")
def cerrarSesion():
    session.clear()

    return redirect(url_for("inicio"))


cargarEstado()


if __name__ == "__main__":
    app.run()