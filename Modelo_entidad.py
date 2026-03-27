# modelado_entidad.py
# Reto de Modelado - Constructor de Entidades
# Modeling Challenge - Entity Constructor
# Unidad 2 - Programacion Estructurada

# diccionario que representa la entidad principal del proyecto: Producto
# dictionary representing the main entity of the project: Product
producto = {
    "id":           101,           # int   - identificador unico / unique identifier
    "nombre":       "Auriculares", # str   - nombre del producto / product name
    "precio_venta": 280000.0,      # float - precio de venta / sale price
    "mejor_costo":  150000.0,      # float - mejor costo proveedor / best supplier cost
    "disponible":   True,          # bool  - si esta disponible / if available
    "mejor_prov":   "Proveedor 1", # str   - proveedor elegido / chosen supplier
    "rentabilidad": 86.67          # float - porcentaje rentabilidad / profitability %
}

print("=" * 50)
print(f"  {'ENTIDAD: PRODUCTO / ENTITY: PRODUCT':^46}")
print("=" * 50)

# imprimir solo las llaves con .keys()
# print only the keys with .keys()
print("\n--- Llaves / Keys ---")
for llave in producto.keys():
    print(f"  {llave}")

# imprimir solo los valores con .values()
# print only the values with .values()
print("\n--- Valores / Values ---")
for valor in producto.values():
    print(f"  {valor}")

# imprimir llaves y valores con .items()
# print keys and values with .items()
print("\n--- Reporte completo / Full report ---")
for llave, valor in producto.items():
    print(f"  {llave.upper():<15} : {valor}")

# demostrar actualizacion de un valor con .update()
# demonstrate updating a value with .update()
print("\n--- Antes de actualizar / Before update ---")
print(f"  disponible : {producto['disponible']}")

producto.update({"disponible": False})

print("\n--- Despues de actualizar / After update ---")
print(f"  disponible : {producto['disponible']}")

print("\n" + "=" * 50)
print(f"  Script ejecutado con exito / Script ran successfully")
print("=" * 50)