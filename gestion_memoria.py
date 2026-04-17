# gestion_memoria.py
# Reto de Logica - Simulador de Memoria Volatil
# Logic Challenge - Volatile Memory Simulator
# Guia Practica N6 - Programacion Estructurada

# =============================================================================
# PASO 1: CREACION - Inicializar lista con 3 elementos base
# STEP 1: CREATION - Initialize list with 3 base elements
# =============================================================================

# se crea la lista inicial con 3 productos
# the initial list is created with 3 products
lista = ["Mouse", "Teclado", "Monitor"]

print("=" * 50)
print(f"  {'SIMULADOR DE MEMORIA VOLATIL':^46}")
print(f"  {'Volatile Memory Simulator':^46}")
print("=" * 50)

print("\n1. Lista inicial / Initial list:")
print(f"   {lista}")

# =============================================================================
# PASO 2: EXPANSION - .append() e .insert()
# STEP 2: EXPANSION - .append() and .insert()
# =============================================================================

# .append() agrega un elemento al FINAL de la lista
# .append() adds an element to the END of the list
lista.append("Auriculares")

# .insert(posicion, elemento) agrega en una posicion especifica
# .insert(position, element) adds at a specific position
# posicion 1 significa que queda de segundo en la lista
# position 1 means it becomes second in the list
lista.insert(1, "Webcam")

print("\n2. Despues de append() e insert() / After append() and insert():")
print(f"   {lista}")
# estado esperado / expected state: ["Mouse", "Webcam", "Teclado", "Monitor", "Auriculares"]

# =============================================================================
# PASO 3: DEPURACION - .remove() y .pop()
# STEP 3: DEBUGGING - .remove() and .pop()
# =============================================================================

# .remove(valor) elimina la primera ocurrencia del valor indicado
# .remove(value) removes the first occurrence of the indicated value
lista.remove("Webcam")

# .pop(posicion) elimina el elemento en esa posicion y lo retorna
# .pop(position) removes the element at that position and returns it
# si no se pasa posicion, elimina el ultimo elemento
# if no position is passed, it removes the last element
elemento_eliminado = lista.pop(0)

print("\n3. Despues de remove() y pop() / After remove() and pop():")
print(f"   Elemento eliminado con pop / Element removed with pop: '{elemento_eliminado}'")
print(f"   {lista}")
# estado esperado / expected state: ["Teclado", "Monitor", "Auriculares"]

# =============================================================================
# PASO 4: ORDENAMIENTO - .sort()
# STEP 4: SORTING - .sort()
# =============================================================================

# .sort() organiza la lista alfabeticamente de forma permanente
# .sort() organizes the list alphabetically permanently
lista.sort()

print("\n4. Despues de sort() / After sort():")
print(f"   {lista}")
# estado esperado / expected state: ["Auriculares", "Monitor", "Teclado"]

# =============================================================================
# PASO 5: BUSQUEDA - if elemento in lista
# STEP 5: SEARCH - if element in lista
# =============================================================================

# buscar si un elemento existe en la lista usando el operador 'in'
# search if an element exists in the list using the 'in' operator
elemento_buscar = "Monitor"

if elemento_buscar in lista:
    # el elemento SI existe en la lista / the element DOES exist in the list
    print(f"\n5. Busqueda / Search: '{elemento_buscar}'")
    print(f"   Encontrado / Found: SI / YES")
    print(f"   Posicion / Position: {lista.index(elemento_buscar)}")
else:
    # el elemento NO existe en la lista / the element does NOT exist in the list
    print(f"\n5. Busqueda / Search: '{elemento_buscar}'")
    print(f"   Encontrado / Found: NO")

# buscar un elemento que no existe / search for an element that doesn't exist
elemento_buscar2 = "Laptop"
if elemento_buscar2 in lista:
    print(f"\n   '{elemento_buscar2}': Encontrado / Found: SI / YES")
else:
    print(f"   '{elemento_buscar2}': Encontrado / Found: NO")

# =============================================================================
# RESUMEN FINAL / FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 50)
print(f"  {'ESTADO FINAL / FINAL STATE':^46}")
print("=" * 50)
print(f"\n  Total elementos / Total elements: {len(lista)}")
print()
for i, item in enumerate(lista, 1):
    print(f"  {i}. {item}")

print()
print("=" * 50)
print(f"  Script ejecutado con exito / Script ran successfully")
print("=" * 50)