# archivos.py
# Modulo para el manejo de archivos CSV (guardar y cargar datos)

import csv
import os

ARCHIVO_MATERIALES = "materiales.csv"


def guardar_materiales(lista_materiales):
    #Guarda la lista de materiales (diccionarios) en un archivo CSV.
    with open(ARCHIVO_MATERIALES, "w", newline="", encoding="utf-8") as archivo:
        campos = ("codigo", "nombre", "unidad", "precio")  # tupla: orden fijo de columnas
        escritor = csv.DictWriter(archivo, fieldnames=campos)
        escritor.writeheader()
        for material in lista_materiales:
            escritor.writerow(material)


def cargar_materiales():
    #Lee el archivo CSV y devuelve una lista de diccionarios.
    lista_materiales = []
    # Condicional: si el archivo no existe, devolvemos la lista vacia
    if not os.path.exists(ARCHIVO_MATERIALES):
        return lista_materiales

    with open(ARCHIVO_MATERIALES, "r", newline="", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:  # Ciclo para recorrer cada fila del CSV
            fila["precio"] = float(fila["precio"])  # convertir texto a numero
            lista_materiales.append(fila)
    return lista_materiales


def guardar_cotizacion(nombre_proyecto, items, subtotal, iva, total):
    #Guarda una cotizacion en su propio archivo CSV.
    #items es una lista de tuplas: (codigo, nombre, unidad, precio, cantidad, importe)
    nombre_archivo = "cotizacion_" + nombre_proyecto.replace(" ", "_") + ".csv"
    with open(nombre_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(["COTIZACION DE MATERIALES - PROTICS"])
        escritor.writerow(["Proyecto:", nombre_proyecto])
        escritor.writerow([])  # fila vacia
        escritor.writerow(["Codigo", "Material", "Unidad", "Precio", "Cantidad", "Importe"])
        for item in items:
            escritor.writerow(item)
        escritor.writerow([])
        escritor.writerow(["", "", "", "", "Subtotal:", subtotal])
        escritor.writerow(["", "", "", "", "IVA:", iva])
        escritor.writerow(["", "", "", "", "TOTAL:", total])
    return nombre_archivo


def listar_cotizaciones():
    #Devuelve la lista (ordenada) de archivos CSV de cotizaciones guardadas.
    archivos_encontrados = []
    for nombre in os.listdir("."):
        if nombre.startswith("cotizacion_") and nombre.endswith(".csv"):
            archivos_encontrados.append(nombre)
    archivos_encontrados.sort()
    return archivos_encontrados


def cargar_cotizacion(nombre_archivo):
    #Lee un archivo CSV de cotizacion y devuelve sus datos.
    #Devuelve: (nombre_proyecto, items, subtotal, iva, total)
    with open(nombre_archivo, "r", newline="", encoding="utf-8") as archivo:
        filas = list(csv.reader(archivo))

    nombre_proyecto = filas[1][1]

    items = []
    indice = 4  # las primeras 4 filas son encabezados, los renglones empiezan aqui
    while filas[indice] != []:
        codigo, nombre, unidad, precio, cantidad, importe = filas[indice]
        items.append((codigo, nombre, unidad, float(precio), float(cantidad), float(importe)))
        indice += 1

    subtotal = float(filas[indice + 1][5])
    iva = float(filas[indice + 2][5])
    total = float(filas[indice + 3][5])

    return nombre_proyecto, items, subtotal, iva, total


def eliminar_cotizacion(nombre_archivo):
    #Elimina el archivo CSV de una cotizacion guardada.
    if os.path.exists(nombre_archivo):
        os.remove(nombre_archivo)
