# prueba_persistencia.py
# Laboratorio de Ciclo de Vida de Datos
# Data Lifecycle Laboratory
# Guia Practica N8 - Programacion Estructurada

import os  # para verificar si el archivo existe / to check if file exists

# =============================================================================
# PASO 1: CREACION CON CONTEXT MANAGER - with open() modo escritura 'w'
# STEP 1: CREATION WITH CONTEXT MANAGER - with open() write mode 'w'
# =============================================================================
# 'w' crea el archivo si no existe y borra el contenido si ya existe
# 'w' creates the file if it doesn't exist and clears content if it already exists
# with open() garantiza que el buffer se vacia y el archivo se cierra correctamente
# with open() guarantees the buffer is flushed and the file is closed correctly

print("=" * 55)
print(f"  {'LABORATORIO DE PERSISTENCIA':^51}")
print(f"  {'Persistence Laboratory':^51}")
print("=" * 55)

print("\nPASO 1 / STEP 1: Creando archivo / Creating file...")

with open("log_sistema.txt", "w", encoding="utf-8") as archivo:
    # escritura de buffers con tres lineas bilingues / buffer writing with three bilingual lines
    # .write() escribe el texto en el buffer de memoria
    # .write() writes the text to the memory buffer
    # al salir del bloque with, Python vacia el buffer automaticamente
    # when exiting the with block, Python automatically flushes the buffer
    archivo.write("=== LOG DEL SISTEMA / SYSTEM LOG ===\n")
    archivo.write("Linea 1: Sistema iniciado correctamente / System started successfully\n")
    archivo.write("Linea 2: Base de datos cargada / Database loaded\n")
    archivo.write("Linea 3: Modulos activos / Active modules: calculos, persistencia, ui\n")
# el archivo se cierra automaticamente al salir del bloque with
# the file closes automatically when exiting the with block

print("  Archivo creado con 3 lineas / File created with 3 lines")
print("  Buffer vaciado y archivo cerrado / Buffer flushed and file closed")

# =============================================================================
# PASO 2: MODO APPEND 'a' - agregar sin borrar lo anterior
# STEP 2: APPEND MODE 'a' - add without deleting previous content
# =============================================================================
# 'a' abre el archivo y pone el cursor al FINAL sin borrar nada
# 'a' opens the file and places the cursor at the END without deleting anything

print("\nPASO 2 / STEP 2: Agregando con modo append / Adding with append mode...")

with open("log_sistema.txt", "a", encoding="utf-8") as archivo:
    # esta linea se agrega AL FINAL del archivo sin borrar las anteriores
    # this line is added AT THE END of the file without deleting the previous ones
    archivo.write("Linea 4 (append): Nuevo registro agregado sin borrar / New record added without deleting\n")
    archivo.write("Linea 5 (append): Archivo cerrado y reabierto / File closed and reopened\n")

print("  2 lineas agregadas en modo append / 2 lines added in append mode")
print("  El contenido anterior NO fue borrado / Previous content was NOT deleted")

# =============================================================================
# PASO 3: LECTURA Y VERIFICACION
# STEP 3: READING AND VERIFICATION
# =============================================================================
# 'r' abre el archivo solo para leer / 'r' opens the file for reading only

print("\nPASO 3 / STEP 3: Leyendo y verificando / Reading and verifying...")

# lista que almacena cada linea del archivo / list that stores each line from the file
lineas = []

with open("log_sistema.txt", "r", encoding="utf-8") as archivo:
    # .readlines() lee todo el archivo y retorna una lista donde cada elemento es una linea
    # .readlines() reads the entire file and returns a list where each element is a line
    lineas = archivo.readlines()

# mostrar el contenido completo / show full content
print()
print("  Contenido del archivo / File content:")
print("  " + "-" * 51)

for i, linea in enumerate(lineas, 1):
    # .strip() elimina el salto de linea \n al final de cada linea
    # .strip() removes the newline \n at the end of each line
    print(f"  [{i}] {linea.strip()}")

print("  " + "-" * 51)
print(f"  Total lineas / Total lines: {len(lineas)}")

# =============================================================================
# RESUMEN FINAL / FINAL SUMMARY
# =============================================================================
print()
print("=" * 55)
print(f"  {'RESUMEN / SUMMARY':^51}")
print("=" * 55)
print(f"  {'Archivo creado / File created':<35} log_sistema.txt")
print(f"  {'Modo escritura / Write mode':<35} 'w' - sobreescribe")
print(f"  {'Modo anexar / Append mode':<35} 'a' - agrega al final")
print(f"  {'Modo lectura / Read mode':<35} 'r' - solo leer")
print(f"  {'Context manager / Context manager':<35} with open()")
print(f"  {'Total lineas / Total lines':<35} {len(lineas)}")
print(f"  {'Buffer vaciado / Buffer flushed':<35} Si / Yes (automatico)")
print()
print(f"  Script ejecutado con exito / Script ran successfully")
print("=" * 55)