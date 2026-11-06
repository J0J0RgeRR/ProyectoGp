import users
import bathrooms
import paper
import parking 
stock = 0
sales = []
running= True

while running:
    role = users.iniciarSesion()

    while True:
        option = users.mostrarMenu(role)

        if option == 0:
            print("Sesión cerrada.")
            break

        elif option == 1:
            stock = bathrooms.registrarCobro(stock, sales)

        elif option == 2:
            parking.seleccionar_servicio()

        elif option == 3:
            print("Cobros a mercaderes pendientes.")

        elif option == 4:
            print("Registro de gastos pendiente.")

        elif option == 5:
            print("Caja pendiente.")

        elif option == 6:
            bathrooms.consultarCobros(sales)
            parking.mostrar_cobros()

        elif option == 7:
            paper.consultarInventario(stock)

        elif option == 8:
            print("Programa finalizado.")
            running = False
            break
        elif option == 9:
            if role == "administrador":
                print("Gestión de mercaderes pendiente.")
        elif option == 10:
            if role == "administrador":
                stock= paper.ingresarRollos(stock)
        
