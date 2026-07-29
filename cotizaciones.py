# cotizaciones.py
# Modulo para crear cotizaciones de materiales para proyectos PROTICS

from fpdf import FPDF

import archivos
import materiales

IVA = 0.19  # 19% de IVA


def menu_cotizaciones(lista_materiales):
    #Submenu con las operaciones disponibles para las cotizaciones.
    while True:
        print("\n--- MENU DE COTIZACIONES ---")
        print("1. Agregar cotizacion")
        print("2. Ver cotizaciones")
        print("3. Eliminar cotizacion")
        print("4. Volver al menu principal")
        opcion = input("Elige una opcion (1-4): ").strip()

        if opcion == "1":
            crear_cotizacion(lista_materiales)
        elif opcion == "2":
            ver_cotizaciones()
        elif opcion == "3":
            eliminar_cotizacion_menu()
        elif opcion == "4":
            break
        else:
            print("Opcion no valida, intenta de nuevo.")


def ver_cotizaciones():
    #Muestra la lista de cotizaciones guardadas y permite abrir una para verla.
    print("\n--- COTIZACIONES GUARDADAS ---")
    lista_archivos = archivos.listar_cotizaciones()

    if len(lista_archivos) == 0:
        print("No hay cotizaciones guardadas.")
        return

    for indice, nombre_archivo in enumerate(lista_archivos, start=1):
        print(f"{indice}. {nombre_archivo}")

    seleccion = input("\nNumero de cotizacion a ver (Enter para volver): ").strip()
    if seleccion == "":
        return

    if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(lista_archivos):
        print("Opcion no valida.")
        return

    nombre_archivo = lista_archivos[int(seleccion) - 1]
    nombre_proyecto, items, subtotal, iva, total = archivos.cargar_cotizacion(nombre_archivo)
    mostrar_cotizacion(nombre_proyecto, items, subtotal, iva, total)
    preguntar_exportar(nombre_proyecto, items, subtotal, iva, total)


def eliminar_cotizacion_menu():
    #Muestra la lista de cotizaciones guardadas y permite eliminar una.
    print("\n--- ELIMINAR COTIZACION ---")
    lista_archivos = archivos.listar_cotizaciones()

    if len(lista_archivos) == 0:
        print("No hay cotizaciones guardadas.")
        return

    for indice, nombre_archivo in enumerate(lista_archivos, start=1):
        print(f"{indice}. {nombre_archivo}")

    seleccion = input("\nNumero de cotizacion a eliminar (Enter para cancelar): ").strip()
    if seleccion == "":
        return

    if not seleccion.isdigit() or int(seleccion) < 1 or int(seleccion) > len(lista_archivos):
        print("Opcion no valida.")
        return

    nombre_archivo = lista_archivos[int(seleccion) - 1]
    confirmacion = input(f"Seguro que deseas eliminar '{nombre_archivo}'? (s/n): ").strip().lower()
    if confirmacion == "s":
        archivos.eliminar_cotizacion(nombre_archivo)
        print("Cotizacion eliminada.")
    else:
        print("Operacion cancelada.")

#Función recursiva para calcular el subtotal de la cotización
def calcular_subtotal(items):
    #Funcion recursiva: suma el importe del primer item mas el subtotal del resto.
    if len(items) == 0:
        return 0
    primer_importe = items[0][5]  # posicion 5 de la tupla = importe
    return primer_importe + calcular_subtotal(items[1:])


def crear_cotizacion(lista_materiales):
    #Crea una cotizacion pidiendo materiales y cantidades al usuario.
    print("\n--- NUEVA COTIZACION ---")

    if len(lista_materiales) == 0:
        print("Primero debes registrar materiales en el catalogo.")
        return

    nombre_proyecto = input("Nombre del proyecto: ").strip()
    items = []  # Lista de tuplas con los renglones de la cotizacion

    # Ciclo while: agregar materiales hasta que el usuario escriba 'fin'
    while True:
        materiales.listar_materiales(lista_materiales)
        codigo = input("\nCodigo del material (o 'fin' para terminar): ").strip().upper()

        if codigo == "FIN":
            break

        material = materiales.buscar_material(lista_materiales, codigo)
        if material is None:
            print("Codigo no encontrado, intenta de nuevo.")
            continue

        try:
            cantidad = float(input("Cantidad: "))
        except ValueError:
            print("Cantidad no valida, intenta de nuevo.")
            continue

        if cantidad <= 0:
            print("La cantidad debe ser mayor que cero.")
            continue

        importe = round(material["precio"] * cantidad, 2)

        # Tupla: un renglon de la cotizacion (no debe modificarse despues)
        item = (material["codigo"], material["nombre"], material["unidad"],
                material["precio"], cantidad, importe)
        items.append(item)
        print(f"Agregado: {material['nombre']} x {cantidad} = ${importe:.2f}")

    if len(items) == 0:
        print("No se agrego ningun material. Cotizacion cancelada.")
        return

    # Calcular el subtotal con la funcion recursiva
    subtotal = round(calcular_subtotal(items), 2)
    iva = round(subtotal * IVA, 2)
    total = round(subtotal + iva, 2)

    mostrar_cotizacion(nombre_proyecto, items, subtotal, iva, total)

    archivo = archivos.guardar_cotizacion(nombre_proyecto, items, subtotal, iva, total)
    print(f"\nCotizacion guardada en el archivo: {archivo}")

    preguntar_exportar(nombre_proyecto, items, subtotal, iva, total)


def construir_texto_cotizacion(nombre_proyecto, items, subtotal, iva, total):
    #Arma el texto de la cotizacion (se usa para mostrarla y para exportarla a TXT).
    lineas = []
    lineas.append("=" * 70)
    lineas.append("COTIZACION DE MATERIALES - PROTICS")
    lineas.append("Proyecto: " + nombre_proyecto)
    lineas.append("=" * 70)
    lineas.append(f"{'Codigo':<8}{'Material':<25}{'Unidad':<8}{'Precio':>9}{'Cant.':>8}{'Importe':>11}")
    lineas.append("-" * 70)
    for item in items:
        codigo, nombre, unidad, precio, cantidad, importe = item  # desempaquetar tupla
        lineas.append(f"{codigo:<8}{nombre:<25}{unidad:<8}{precio:>9.2f}{cantidad:>8.1f}{importe:>11.2f}")
    lineas.append("-" * 70)
    lineas.append(f"{'Subtotal:':>59}{subtotal:>11.2f}")
    lineas.append(f"{'IVA (19%):':>59}{iva:>11.2f}")
    lineas.append(f"{'TOTAL:':>59}{total:>11.2f}")
    lineas.append("=" * 70)
    return "\n".join(lineas)


def mostrar_cotizacion(nombre_proyecto, items, subtotal, iva, total):
    """Imprime la cotizacion en pantalla con formato de tabla."""
    print("\n" + construir_texto_cotizacion(nombre_proyecto, items, subtotal, iva, total))


def preguntar_exportar(nombre_proyecto, items, subtotal, iva, total):
    #Pregunta al usuario si desea exportar la cotizacion a TXT o PDF.
    print("\n¿Deseas exportar esta cotizacion?")
    print("1. Exportar a TXT")
    print("2. Exportar a PDF")
    print("3. No exportar")
    opcion = input("Elige una opcion (1-3): ").strip()

    if opcion == "1":
        archivo = exportar_txt(nombre_proyecto, items, subtotal, iva, total)
        print(f"Cotizacion exportada en: {archivo}")
    elif opcion == "2":
        archivo = exportar_pdf(nombre_proyecto, items, subtotal, iva, total)
        print(f"Cotizacion exportada en: {archivo}")
    else:
        print("No se exporto la cotizacion.")


def exportar_txt(nombre_proyecto, items, subtotal, iva, total):
    #Exporta la cotizacion a un archivo de texto plano (.txt).
    nombre_archivo = "cotizacion_" + nombre_proyecto.replace(" ", "_") + ".txt"
    texto = construir_texto_cotizacion(nombre_proyecto, items, subtotal, iva, total)
    with open(nombre_archivo, "w", encoding="utf-8") as archivo:
        archivo.write(texto)
    return nombre_archivo


def exportar_pdf(nombre_proyecto, items, subtotal, iva, total):
    #Exporta la cotizacion a un archivo PDF (.pdf) usando la libreria fpdf2.
    nombre_archivo = "cotizacion_" + nombre_proyecto.replace(" ", "_") + ".pdf"

    anchos = (20, 62, 20, 22, 18, 26)

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "COTIZACION DE MATERIALES - PROTICS", align="C")
    pdf.ln(10)

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 8, f"Proyecto: {nombre_proyecto}")
    pdf.ln(12)

    pdf.set_font("Helvetica", "B", 10)
    encabezados = ("Codigo", "Material", "Unidad", "Precio", "Cant.", "Importe")
    for ancho, texto in zip(anchos, encabezados):
        pdf.cell(ancho, 8, texto, border=1)
    pdf.ln(8)

    pdf.set_font("Helvetica", "", 10)
    for item in items:
        codigo, nombre, unidad, precio, cantidad, importe = item  # desempaquetar tupla
        valores = (codigo, nombre, unidad, f"${precio:.2f}", f"{cantidad:.1f}", f"${importe:.2f}")
        for ancho, texto in zip(anchos, valores):
            pdf.cell(ancho, 8, texto, border=1)
        pdf.ln(8)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(0, 8, f"Subtotal: ${subtotal:.2f}", align="R")
    pdf.ln(8)
    pdf.cell(0, 8, f"IVA (19%): ${iva:.2f}", align="R")
    pdf.ln(8)
    pdf.cell(0, 8, f"TOTAL: ${total:.2f}", align="R")

    pdf.output(nombre_archivo)
    return nombre_archivo
