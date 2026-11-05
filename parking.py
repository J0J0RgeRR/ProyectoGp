
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
