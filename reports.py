from datetime import date, timedelta

import files


def calcularPeriodo(reportType, referenceDate):
    try:
        selectedDate = date.fromisoformat(referenceDate)

    except (ValueError, TypeError):
        return None, None, "Seleccioná una fecha válida."

    if reportType == "diario":
        startDate = selectedDate
        endDate = selectedDate

    elif reportType == "semanal":
        startDate = selectedDate - timedelta(days=selectedDate.weekday())
        endDate = startDate + timedelta(days=6)

    elif reportType == "quincenal" or reportType == "mensual":
        firstDay = selectedDate.replace(day=1)

        if selectedDate.month == 12:
            nextMonth = date(selectedDate.year + 1, 1, 1)
        else:
            nextMonth = date(selectedDate.year, selectedDate.month + 1, 1)

        lastDay = nextMonth - timedelta(days=1)

        if reportType == "mensual":
            startDate = firstDay
            endDate = lastDay

        elif selectedDate.day <= 15:
            startDate = firstDay
            endDate = selectedDate.replace(day=15)

        else:
            startDate = selectedDate.replace(day=16)
            endDate = lastDay

    else:
        return None, None, "Seleccioná un tipo de reporte válido."

    return startDate, endDate, None


def filtrarMovimientos(records, startDate, endDate):
    selectedRecords = []

    for record in records:
        try:
            movementDate = date.fromisoformat(record.get("date", ""))

        except (ValueError, TypeError):
            return None, "Hay movimientos sin una fecha válida. Revisá los registros."

        if startDate <= movementDate <= endDate:
            selectedRecord = record.copy()
            selectedRecord.pop("siguiente", None)
            selectedRecords.append(selectedRecord)

    return selectedRecords, None


def sumarMontos(records, field):
    total = 0

    for record in records:
        total = total + record[field]

    total = round(total, 2)

    return total


def generarReporte(reportType, referenceDate, sales, parkingRecords, merchantPayments, expenseRecords):
    startDate, endDate, error = calcularPeriodo(reportType, referenceDate)

    if error is not None:
        return None, error

    bathroomSales, error = filtrarMovimientos(sales, startDate, endDate)

    if error is not None:
        return None, error

    parkingSales, error = filtrarMovimientos(parkingRecords, startDate, endDate)

    if error is not None:
        return None, error

    merchantSales, error = filtrarMovimientos(merchantPayments, startDate, endDate)

    if error is not None:
        return None, error

    expenses, error = filtrarMovimientos(expenseRecords, startDate, endDate)

    if error is not None:
        return None, error

    bathroomIncome = sumarMontos(bathroomSales, "price")
    parkingIncome = sumarMontos(parkingSales, "total")
    merchantIncome = sumarMontos(merchantSales, "amount")
    totalExpenses = sumarMontos(expenses, "amount")

    totalIncome = bathroomIncome + parkingIncome + merchantIncome
    totalIncome = round(totalIncome, 2)

    netIncome = totalIncome - totalExpenses
    netIncome = round(netIncome, 2)

    report = {
        "type": reportType,
        "startDate": startDate.isoformat(),
        "endDate": endDate.isoformat(),
        "bathroomIncome": bathroomIncome,
        "parkingIncome": parkingIncome,
        "merchantIncome": merchantIncome,
        "totalIncome": totalIncome,
        "totalExpenses": totalExpenses,
        "netIncome": netIncome,
        "bathroomSales": bathroomSales,
        "parkingSales": parkingSales,
        "merchantPayments": merchantSales,
        "expenses": expenses
    }

    return report, None


def guardarReporte(report):
    fileName = "reportes/" + report["type"] + "_" + report["startDate"] + "_" + report["endDate"] + ".json"

    error = files.guardarDatos(fileName, report)

    return fileName, error