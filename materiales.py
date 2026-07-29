# materiales.py
# Modulo para gestionar el catalogo de materiales

import csv
import archivos

# Tupla: las unidades de medida permitidas (las tuplas no se pueden modificar)
UNIDADES = ("pieza", "metro", "caja", "rollo", "litro", "kg")

def agregar_material(lista_materiales):
    #Pide los datos de un material y lo agrega a la lista.
    print("\n--- AGREGAR MATERIAL ---")
    codigo = input("Codigo del material: ").strip().upper()

    # Conjunto: se arma el set de codigos existentes para revisar duplicados
    codigos_existentes = {material["codigo"] for material in lista_materiales}
    if codigo in codigos_existentes:
        print("Error: ya existe un material con ese codigo.")
        return

    nombre = input("Nombre del material: ").strip()

    print("Unidades disponibles:", UNIDADES)
    unidad = input("Unidad de medida: ").strip().lower()
    if unidad not in UNIDADES:
        print("Unidad no valida, se usara 'pieza'.")
        unidad = "pieza"

    try:
        precio = float(input("Precio unitario: $"))
    except ValueError:
        print("Precio no valido, se usara 0.")
        precio = 0.0

    # Diccionario: cada material se guarda como un diccionario
    material = {
        "codigo": codigo,
        "nombre": nombre,
        "unidad": unidad,
        "precio": precio,
    }
    lista_materiales.append(material)
    archivos.guardar_materiales(lista_materiales)
    print("Material agregado correctamente.")


def listar_materiales(lista_materiales):
    #Muestra todos los materiales en forma de tabla.
    print("\n--- CATALOGO DE MATERIALES ---")
    if len(lista_materiales) == 0:
        print("No hay materiales registrados.")
        return

    print(f"{'Codigo':<10}{'Nombre':<30}{'Unidad':<10}{'Precio':>10}")
    print("-" * 60)
    for material in lista_materiales:  # Ciclo para recorrer la lista
        print(f"{material['codigo']:<10}{material['nombre']:<30}"
              f"{material['unidad']:<10}{material['precio']:>10.2f}")


def buscar_material(lista_materiales, codigo):
    #Busca un material por su codigo. Devuelve el diccionario o None.
    for material in lista_materiales:
        if material["codigo"] == codigo:
            return material
    return None


def eliminar_material(lista_materiales):
    """Elimina un material del catalogo por su codigo."""
    print("\n--- ELIMINAR MATERIAL ---")
    codigo = input("Codigo del material a eliminar: ").strip().upper()
    material = buscar_material(lista_materiales, codigo)

    if material is None:
        print("No se encontro un material con ese codigo.")
    else:
        lista_materiales.remove(material)
        archivos.guardar_materiales(lista_materiales)
        print("Material '" + material["nombre"] + "' eliminado.")
