def iniciarSesion():
    while True:
        print("\n--- INICIAR SESIÓN ---")

        username = input("Usuario: ").strip()
        password = input("Contraseña: ")

        if username == "" or password.strip() == "":
            print("Debe completar ambos campos.")

        elif username == "admin" and password == "admin123":
            return "administrador"

        elif username == "trabajador" and password == "trabajador123":
            return "trabajador"

        else:
            print("Usuario o contraseña incorrectos.")

def mostrarMenu(role):
    if role != "administrador" and role != "trabajador":
        print("Perfil no válido.")
        return None

    while True:
        print(f"\n--- PANEL DE {role.upper()} ---")
        print("1. Cobros de baños")
        print("2. Cobros de parqueo")
        print("3. Cobrar a mercaderes")
        print("4. Registrar gastos")
        print("5. Caja")

        if role == "administrador":
            print("6. Reportes diarios, semanales, quincenales y mensuales")
        else:
            print("6. Reporte del dia actual")
        print("7. Consultar inventario de papel")
        print("8. Finalizar el programa")

        if role == "administrador":

            print("9. Gestionar mercaderes")
            print("10. Ingresar rollos de papel")
            limit = 10
        else:
            limit = 8

        print("0. Cerrar sesión")

        try:
            option = int(input("Seleccione una opción: "))

            if option >= 0 and option <= limit:
                return option
            else:
                print(f"Seleccione una opción del 0 al {limit}.")

        except ValueError:
            print("Debe ingresar un número entero.")