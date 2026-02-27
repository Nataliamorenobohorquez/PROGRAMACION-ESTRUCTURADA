# Nombre: Natalia Moreno
# Proyecto: Sistema de Ventas

while True:
    print("\n=================================")
    print("        SISTEMA DE VENTAS")
    print("=================================")
    print("1. Registrar venta")
    print("2. Calcular total con descuento")
    print("3. Salir")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        producto = input("Ingrese nombre del producto: ")
        precio = float(input("Ingrese precio del producto: "))
        cantidad = int(input("Ingrese cantidad: "))

        subtotal = precio * cantidad
        iva = subtotal * 0.19
        total = subtotal + iva

        print("\n----- FACTURA -----")
        print(f"Producto: {producto}")
        print(f"Subtotal: {subtotal}")
        print(f"IVA (19%): {iva}")
        print(f"Total a pagar: {total}")

    elif opcion == "2":
        precio = float(input("Ingrese precio del producto: "))
        descuento = float(input("Ingrese porcentaje de descuento: "))

        valor_descuento = precio * (descuento / 100)
        total = precio - valor_descuento

        print(f"Descuento aplicado: {valor_descuento}")
        print(f"Total con descuento: {total}")

    elif opcion == "3":
        print("Saliendo del sistema...")
        break

    else:
        print("!!! ERROR: Opción inválida. Intente de nuevo.")