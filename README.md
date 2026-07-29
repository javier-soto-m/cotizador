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
