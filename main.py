# main.py
# Programa principal: Sistema de cotizaciones de materiales para proyectos PROTICS
# Para ejecutar: python main.py

import archivos
import materiales
import cotizaciones


def mostrar_menu():
    """Muestra las opciones del menu principal."""
    print("\n========================================")
    print("  COTIZADOR DE MATERIALES - PROTICS")
    print("========================================")
    print("1. Agregar material al catalogo")
    print("2. Ver catalogo de materiales")
    print("3. Eliminar material")
    print("4. Cotizaciones (crear, ver, eliminar)")
    print("5. Salir")


def main():
    # Al iniciar, cargamos los materiales guardados en el archivo CSV
    lista_materiales = archivos.cargar_materiales()
    print(f"Se cargaron {len(lista_materiales)} materiales del archivo.")

    # Ciclo principal del programa
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion (1-5): ").strip()

        # Condicionales para cada opcion del menu
        if opcion == "1":
            materiales.agregar_material(lista_materiales)
        elif opcion == "2":
            materiales.listar_materiales(lista_materiales)
        elif opcion == "3":
            materiales.eliminar_material(lista_materiales)
        elif opcion == "4":
            cotizaciones.menu_cotizaciones(lista_materiales)
        elif opcion == "5":
            print("Hasta luego!")
            break
        else:
            print("Opcion no valida, intenta de nuevo.")

main()
