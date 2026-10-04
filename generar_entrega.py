# -*- coding: utf-8 -*-
"""
Generador del documento de entrega (Canvas) y del ZIP final.
Utiliza python-docx. Ejecutar DESDE la carpeta del proyecto:

    python generar_entrega.py

Produce:
    fernandez_tarea_u3/entrega_tarea_u3_fernandez.docx
    fernandez_tarea_u3/*.png, *.py, README.md
    fernandez_tarea_u3.zip

Antes de ejecutar, completa los datos de la seccion CONFIGURACION.
"""

import os
import shutil
import zipfile
from datetime import date

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt

# ---------------------------------------------------------------------------
# CONFIGURACION: completa aqui tus datos
# ---------------------------------------------------------------------------
ALUMNO = "Alejo Fernandez"
MATRICULA = "5181387"
REPOSITORIO = "https://github.com/alejof30494-design/taller5g-unidad3-fernandez"
MATERIA = "Taller de Programación de 5.ª Generación I"
DOCENTE = "Prof. Mgtr. Alberto F. Giménez Méndez"
INSTITUCION = "Universidad Americana · Facultad de Ciencias y Tecnología"
CARRERA = "Ingeniería en Sistemas / Ciencias de la Computación"

CARPETA = "fernandez_tarea_u3"
ZIP = "fernandez_tarea_u3.zip"
DOCX = "entrega_tarea_u3_fernandez.docx"

# Archivos que se copian al ZIP (codigo e imagenes pedidas + extensiones).
ARCHIVOS = [
    "ejercicio1_casa.py",
    "ejercicio2_roseta.py",
    "animacion_roseta.py",
    "casa.png",
    "roseta_12.png",
    "roseta_24.png",
    "roseta_36.png",
    "roseta_salto5.png",
    "roseta_salto7.png",
    "rosetas_animacion.gif",
    "README.md",
]

# Imagenes insertadas en el documento con su epigrafe.
IMAGENES = [
    ("casa.png", "Ejercicio 1: casa estilizada trazada con DDA (600 × 500 px)."),
    ("roseta_12.png", "Ejercicio 2: roseta con N = 12 (66 líneas con Bresenham)."),
    ("roseta_24.png", "Ejercicio 2: roseta con N = 24 (276 líneas con Bresenham)."),
    ("roseta_36.png", "Ejercicio 2: roseta con N = 36 (630 líneas con Bresenham)."),
    ("roseta_salto5.png", "Extensión: roseta estrellada uniendo puntos de salto 5."),
    ("roseta_salto7.png", "Extensión: roseta estrellada uniendo puntos de salto 7."),
]

DESCRIPCION_1 = (
    "En el Ejercicio 1 se implementó la función dda(pixels, x0, y0, x1, y1, "
    "color, ancho, alto) con la firmaBluy vista en clase: el número de pasos se "
    "calcula como la proyección del segmento sobre el eje de mayor "
    "desplazamiento (regla del píxel dominante) y en cada paso se redondea la "
    "coordenada al píxel entero más cercano, con recorte contra los bordes "
    "del frame buffer. Sobre esa única función se construyeron las primitivas "
    "dibujar_rectangulo, dibujar_triangulo, dibujar_puerta, dibujar_ventana, "
    "dibujar_sol y dibujar_linea_piso, cada una responsible de un elemento de "
    "la composición, de modo que el cuerpo de la casa, el techo, la puerta, las "
    "dos ventanas, el sol de 12 rayos y la línea de piso quedan "
    "programados como módulos independientes. Los rellidos interiores "
    "(paredes, vidrio, puerta, césped y disco solar) también se realizaron con "
    "dda(), trazando una línea horizontal por fila."
)

DESCRIPCION_2 = (
    "En el Ejercicio 2 se implementó la función bresenham(pixels, x0, y0, x1, "
    "y1, color, ancho, alto) con aritmética entera: dx = |x1 − x0|, "
    "dy = −|y1 − y0|, error inicial err = dx + dy y la regla e2 = 2·err "
    "para decidir el desplazamiento en X y/o en Y, con las variables de sentido "
    "sx y sy que permiten trazar líneas con coordenadas decrecientes. La "
    "función generar_puntos_circulo(cx, cy, radio, n) distribuyó los n puntos "
    "equiespaciados de la circunferencia imaginaria mediante 2·π·i/n con "
    "math.cos y math.sin, y dibujar_roseta(pixels, puntos, ancho, alto) conectó "
    "cada punto con todos los demás (276 líneas para N = 24). El color de cada "
    "línea se obtiene del punto medio de la cuerda: el matiz se calcula con el "
    "ángulo respecto del centro (HSV recorre todo el espectro) y la luminosidad "
    "con la distancia normalizada al centro, lo que produce el gradiente "
    "radial pedido."
)

OBSERVACIONES = [
    "Dificultades: al principio la puerta y las ventanas quedaban solo con su "
    "contorno y se veía el color del cielo a través de ellas; se resolvió "
    "rellenando cada superficie con líneas horizontales trazadas con dda(). "
    "También hubo que corregir el césped, que dejaba huecos porque las bandas "
    "de gradiente se dibujaban cada 5 píxeles en lugar de en cada fila.",

    "Aprendizajes: quedé claro por qué DDA necesita aritmética de punto "
    "flotante y redondeo en cada paso, mientras que Bresenham resuelve el "
    "mismo problema solo con enteros, y por qué el algoritmo de Bresenham es "
    "más rápido cuando la línea es muy inclinada. También entendí que el "
    "frame buffer es simplemente una matriz de píxeles sobre la que se puede "
    "escribir coordenada por coordenada.",

    "Extensiones voluntarias implementadas: (1) en el Ejercicio 1 se "
    "agregaron árboles con tronco rectangular y copa triangular, dos nubes "
    "compuestas por líneas cortas, humo saliendo de la chimenea y gradientes "
    "de color en el techo y el césped. (2) En el Ejercicio 2 se generaron dos "
    "rosetas estrelladas que conectan únicamente puntos no adyacentes (saltos "
    "de 5 y de 7) y un script adicional que produce 20 rosetas con N "
    "creciente (de 5 a 24) combinadas en un GIF animado.",

    "Para ejecutar los scripts hace falta tener instalado Pillow "
    "(pip install Pillow). Los tres scripts corren sin errores y generan todas "
    "las imágenes en la carpeta donde se ejecutan.",
]


def construir_docx():
    """Crea el documento Word con encabezado, enlace, descripciones,
    imágenes y observaciones."""
    doc = Document()

    # --- Encabezado ---
    doc.add_heading(MATERIA, level=0)
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run("Tarea práctica · Unidad III: Conversión por rastreo "
                    "(DDA y Bresenham)")
    run.bold = True

    for linea in [INSTITUCION, CARRERA, ""]:
        doc.add_paragraph(linea)

    datos = doc.add_table(rows=0, cols=2)
    datos.style = "Table Grid"
    for etiqueta, valor in [
        ("Alumno", ALUMNO),
        ("Matrícula", MATRICULA),
        ("Docente", DOCENTE),
        ("Fecha", date.today().strftime("%d/%m/%Y")),
        ("Asunto", "Entrega de la Tarea práctica de la Unidad III"),
    ]:
        fila = datos.add_row().cells
        fila[0].text = etiqueta
        fila[1].text = valor
        for parrafo in fila[0].paragraphs:
            for r in parrafo.runs:
                r.bold = True

    # --- Enlace al repositorio ---
    doc.add_heading("1. Repositorio Git", level=1)
    doc.add_paragraph(
        "El código fuente y las imágenes generadas se encuentran en el "
        "repositorio:"
    )
    doc.add_paragraph(REPOSITORIO)
    doc.add_paragraph(
        "El repositorio es público. Si fuera privado, el docente fue "
        "agregado como colaborador (usuario alberto-gimenez)."
    )

    # --- Descripción de la solución ---
    doc.add_heading("2. Descripción de la solución", level=1)

    doc.add_heading("Ejercicio 1 – Composición geométrica con DDA", level=2)
    doc.add_paragraph(DESCRIPCION_1)

    doc.add_heading("Ejercicio 2 – Composición dinámica con Bresenham", level=2)
    doc.add_paragraph(DESCRIPCION_2)

    # --- Imágenes generadas ---
    doc.add_heading("3. Imágenes generadas", level=1)
    for archivo, epigrafe in IMAGENES:
        if not os.path.exists(archivo):
            continue
        doc.add_picture(archivo, width=Inches(5.5))
        doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
        pie = doc.add_paragraph(epigrafe)
        pie.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pie.runs[0].italic = True
        pie.runs[0].font.size = Pt(9)

    # --- Observaciones ---
    doc.add_heading("4. Observaciones personales", level=1)
    for parrafo in OBSERVACIONES:
        doc.add_paragraph(parrafo, style="List Bullet")

    doc.save(DOCX)
    print(f"{DOCX} generado correctamente")


def empaquetar():
    """Crea la carpeta de entrega y la comprime en ZIP."""
    if os.path.isdir(CARPETA):
        shutil.rmtree(CARPETA)
    os.makedirs(CARPETA)

    for archivo in ARCHIVOS + [DOCX]:
        if os.path.exists(archivo):
            shutil.copy2(archivo, os.path.join(CARPETA, archivo))

    if os.path.exists(ZIP):
        os.remove(ZIP)
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for nombre in os.listdir(CARPETA):
            z.write(os.path.join(CARPETA, nombre), os.path.join(CARPETA, nombre))

    print(f"{CARPETA}/ creado con {len(os.listdir(CARPETA))} archivos")
    print(f"{ZIP} generado correctamente")


if __name__ == "__main__":
    construir_docx()
    empaquetar()