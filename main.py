import paper

stock = 0

units = paper.ingresarRollos()
stock = stock + units

print(f"Unidades ingresadas: {units}")
print(f"Unidades disponibles: {stock}")