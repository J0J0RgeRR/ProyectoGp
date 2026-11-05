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