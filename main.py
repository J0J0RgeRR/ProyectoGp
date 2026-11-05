import bathrooms as bath
option = bath.seleccionarServicio()

if option == 4:
    print("Regresando...")
else:
    price= bath.calcularPrecio(option)
    confirmed = bath.confirmarCobro(price)
    if confirmed:
        print("Cobro finalizado")
    else:
        print("Cobro cancelado")