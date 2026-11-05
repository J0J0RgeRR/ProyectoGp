import bathrooms as bath
option = bath.seleccionarServicio()

if option == 4:
    print("Regresando...")
else:
    print(f"Servicio seleccionado: {option}")
    price= bath.calcularPrecio(option)
    print(f"Total a pagar: C${price}")