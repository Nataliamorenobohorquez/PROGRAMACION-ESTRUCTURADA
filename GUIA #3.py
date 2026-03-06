# --- FUNCIONES ---

def saludar_usuario():
    nombre = input("Ingrese su nombre: ")
    print(f"\n*** Bienvenido {nombre} al sistema ***")


def calcular_iva():
    monto = float(input("Ingrese el monto: "))
    iva = monto * 0.19
    print(f"El IVA es: {iva}")


def mostrar_menu():
    print("\n----- MENÚ -----")
    print("1. Saludar")
    print("2. Calcular IVA")
    print("3. Salir")


# --- PROGRAMA PRINCIPAL ---

while True:

    mostrar_menu()
    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        saludar_usuario()

    elif opcion == "2":
        calcular_iva()

    elif opcion == "3":
        print("Saliendo del sistema...")
        break

    else:
        print("Opción no válida")