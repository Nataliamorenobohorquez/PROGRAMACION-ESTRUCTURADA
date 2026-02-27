# CÓDIGO BASE - PROGRAMACIÓN ESTRUCTURADA
# Estructura de menú con persistencia y validación

while True:  # Ciclo para que el programa no se cierre
    print("\n================================")
    print("   SISTEMA DE GESTIÓN BASE")
    print("================================")
    print("1. Saludar")
    print("2. Calcular Suma")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        nombre = input("Ingrese su nombre: ")
        print(f"Hola {nombre}, bienvenido al sistema.")

    elif opcion == "2":
        n1 = float(input("Ingrese primer número: "))
        n2 = float(input("Ingrese segundo número: "))
        resultado = n1 + n2
        print(f"El resultado de la suma es: {resultado}")

    elif opcion == "3":
        print("Saliendo del programa...")
        break  # Termina la ejecución

    else:
        print("!!! ERROR: Opción inválida. Intente de nuevo.")