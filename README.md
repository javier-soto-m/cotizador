# Cotizador de Materiales - PROTICS

Sistema de consola en Python para gestionar un catálogo de materiales y generar cotizaciones de proyectos, con exportación a TXT y PDF.

## Descripción

- Catálogo de materiales (código, nombre, unidad, precio) guardado en `materiales.csv`.
- Cotizaciones: se eligen materiales y cantidades; el sistema calcula subtotal, IVA (19%) y total, y guarda el resultado en `cotizacion_<proyecto>.csv`.
- Exportación de cada cotización a `.txt` o `.pdf`.

## Módulos

| Módulo | Responsabilidad |
|---|---|
| `main.py` | Punto de entrada y menú principal. |
| `materiales.py` | Alta, listado, búsqueda y eliminación de materiales. |
| `cotizaciones.py` | Creación, cálculo, listado, eliminación y exportación de cotizaciones. |
| `archivos.py` | Lectura/escritura de los archivos CSV. |

## Estructuras de datos

- **Lista**: catálogo de materiales e ítems de una cotización.
- **Diccionario**: cada material (`codigo`, `nombre`, `unidad`, `precio`).
- **Tupla**: unidades válidas, columnas del CSV y cada renglón de cotización (dato fijo).
- **Conjunto**: códigos existentes, para detectar duplicados al agregar un material.
- **Recursión**: `calcular_subtotal()` suma los importes de la cotización llamándose a sí misma.

## Funcionalidades

- Agregar, listar y eliminar materiales (con validaciones).
- Crear, ver y eliminar cotizaciones.
- Exportar cotización a TXT o PDF.
- Persistencia en CSV (catálogo y cotizaciones).

## Ejecución

```bash
pip install -r requirement.txt
python main.py
```

## Archivos de ejemplo

- `materiales.csv`: catálogo de entrada.
- `cotizacion_Red_Aula_3.csv`, `cotizacion_Estacion_FotoVoltaica.csv`: cotizaciones generadas por el sistema.

## Evidencia de funcionamiento

Ejecución real de `python main.py`: se consulta el catálogo, se crea una cotización de dos materiales, se calcula el subtotal, IVA y total, y se exporta a TXT.

```
Se cargaron 5 materiales del archivo.

========================================
  COTIZADOR DE MATERIALES - PROTICS
========================================
1. Agregar material al catalogo
2. Ver catalogo de materiales
3. Eliminar material
4. Cotizaciones (crear, ver, eliminar)
5. Salir
Elige una opcion (1-5): 2

--- CATALOGO DE MATERIALES ---
Codigo    Nombre                        Unidad        Precio
------------------------------------------------------------
CAB01     Cable UTP cat 6               metro           8.50
RJ45      Conector RJ45                 pieza           3.00
P001      100X100X3mm                   metro        9400.00
P003      sdhs                          pieza          25.00
P005      fhk                           metro          45.00

Elige una opcion (1-5): 4

--- MENU DE COTIZACIONES ---
1. Agregar cotizacion
2. Ver cotizaciones
3. Eliminar cotizacion
4. Volver al menu principal
Elige una opcion (1-4): 1

--- NUEVA COTIZACION ---
Nombre del proyecto: Red Aula 3 Demo

Codigo del material (o 'fin' para terminar): CAB01
Cantidad: 50
Agregado: Cable UTP cat 6 x 50.0 = $425.00

Codigo del material (o 'fin' para terminar): RJ45
Cantidad: 20
Agregado: Conector RJ45 x 20.0 = $60.00

Codigo del material (o 'fin' para terminar): fin

======================================================================
COTIZACION DE MATERIALES - PROTICS
Proyecto: Red Aula 3 Demo
======================================================================
Codigo  Material                 Unidad     Precio   Cant.    Importe
----------------------------------------------------------------------
CAB01   Cable UTP cat 6          metro        8.50    50.0     425.00
RJ45    Conector RJ45            pieza        3.00    20.0      60.00
----------------------------------------------------------------------
                                                  Subtotal:     485.00
                                                 IVA (19%):      92.15
                                                     TOTAL:     577.15
======================================================================

Cotizacion guardada en el archivo: cotizacion_Red_Aula_3_Demo.csv

¿Deseas exportar esta cotizacion?
1. Exportar a TXT
2. Exportar a PDF
3. No exportar
Elige una opcion (1-3): 1
Cotizacion exportada en: cotizacion_Red_Aula_3_Demo.txt
```

El archivo `cotizacion_Red_Aula_3_Demo.txt` exportado queda así:

```
======================================================================
COTIZACION DE MATERIALES - PROTICS
Proyecto: Red Aula 3 Demo
======================================================================
Codigo  Material                 Unidad     Precio   Cant.    Importe
----------------------------------------------------------------------
CAB01   Cable UTP cat 6          metro        8.50    50.0     425.00
RJ45    Conector RJ45            pieza        3.00    20.0      60.00
----------------------------------------------------------------------
                                                  Subtotal:     485.00
                                                 IVA (19%):      92.15
                                                     TOTAL:     577.15
======================================================================
```
