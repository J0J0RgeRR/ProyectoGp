import json
import os


dataFolder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def cargarDatos(fileName):
    path = os.path.join(dataFolder, fileName)

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data, None

    except FileNotFoundError:
        return None, None

    except (json.JSONDecodeError, UnicodeError):
        return None, "El archivo " + fileName + " no contiene un JSON válido."

    except OSError:
        return None, "No se pudo leer el archivo " + fileName + "."


def guardarDatos(fileName, data):
    path = os.path.join(dataFolder, fileName)
    temporaryPath = path + ".tmp"

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(temporaryPath, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4, allow_nan=False)

        os.replace(temporaryPath, path)

        return None

    except (OSError, TypeError, ValueError):
        return "No se pudo guardar el archivo " + fileName + "."