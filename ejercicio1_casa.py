# -*- coding: utf-8 -*-
"""
Ejercicio 1 - Composición geométrica con DDA
Tarea práctica Unidad III - Conversión por rastreo
Universidad Americana - Taller de Programación de 5.ª Generación I

Dibuja una casa estilizada (vista frontal) sobre un lienzo de 600 x 500 px
utilizando exclusivamente la función dda() para trazar todos los segmentos.

Salida: casa.png
"""

from PIL import Image
import math


# ---------------------------------------------------------------------------
# 1. Algoritmo DDA (Digital Differential Analyzer)
# ---------------------------------------------------------------------------
# Reutiliza la funcion tal como fue presentada en clase, sin modificar su
# firma: dda(pixels, x0, y0, x1, y1, color, ancho, alto)
#
# La idea: se recorre el segmento en pasos de 1/2 pasos, donde "pasos" es la
# proyeccion del segmento en el eje de mayor desplazamiento. En cada paso se
# redondea la coordenada al pixel entero mas cercano y se escribe el color.
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una recta entre (x0,y0) y (x1,y1) con el algoritmo DDA."""
    # Se convierten las coordenadas a enteros: el frame buffer solo admite pixeles.
    x0 = int(round(x0))
    y0 = int(round(y0))
    x1 = int(round(x1))
    y1 = int(round(y1))

    dx = x1 - x0
    dy = y1 - y0

    # Numero de pasos = valor maximo absoluto (regla del pixel dominante).
    pasos = int(max(abs(dx), abs(dy)))

    # Caso degenerado: el segmento es un unico punto.
    if pasos == 0:
        if 0 <= x0 < ancho and 0 <= y0 < alto:
            pixels[x0, y0] = color
        return

    # Incremento constante por paso en cada eje.
    dx_paso = dx / pasos
    dy_paso = dy / pasos

    for i in range(pasos + 1):
        x = int(round(x0 + i * dx_paso))
        y = int(round(y0 + i * dy_paso))
        # Recorte (clipping) contra los bordes del lienzo.
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color


# ---------------------------------------------------------------------------
# 2. Utilidades de color
# ---------------------------------------------------------------------------
def interpolar_color(color_a, color_b, t):
    """Interpola linealmente dos colores RGB. t va de 0.0 a 1.0."""
    t = max(0.0, min(1.0, t))
    return (
        int(color_a[0] + (color_b[0] - color_a[0]) * t),
        int(color_a[1] + (color_b[1] - color_a[1]) * t),
        int(color_a[2] + (color_b[2] - color_a[2]) * t),
    )


def dibujar_linea_degradada(pixels, x0, y0, x1, y1, color_a, color_b,
                            ancho, alto, tramos=60):
    """Linea con gradiente: divide el segmento en tramos y usa dda() en cada
    uno, interpolando el color de un tramo al siguiente (extension voluntaria)."""
    for k in range(tramos):
        t0 = k / tramos
        t1 = (k + 1) / tramos
        xa = x0 + (x1 - x0) * t0
        ya = y0 + (y1 - y0) * t0
        xb = x0 + (x1 - x0) * t1
        yb = y0 + (y1 - y0) * t1
        color = interpolar_color(color_a, color_b, (t0 + t1) / 2.0)
        dda(pixels, xa, ya, xb, yb, color, ancho, alto)


# ---------------------------------------------------------------------------
# 3. Primitivas de la composicion (cada elemento = una funcion)
# ---------------------------------------------------------------------------
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Rectangulo de 4 lineas: superior, inferior, izquierda y derecha."""
    dda(pixels, x0, y0, x1, y0, color, ancho, alto)   # lado superior
    dda(pixels, x1, y0, x1, y1, color, ancho, alto)   # lado derecho
    dda(pixels, x1, y1, x0, y1, color, ancho, alto)   # lado inferior
    dda(pixels, x0, y1, x0, y0, color, ancho, alto)   # lado izquierdo


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Triangulo de 3 lineas que conectan los tres vertices."""
    dda(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    dda(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    dda(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def rellenar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Rellena un rectangulo con lineas horizontales trazadas con dda().

    Se usa para que el interior de la puerta, las ventanas y las paredes no
    quede transparente (solo con el color del cielo de fondo).
    """
    if x1 < x0:
        x0, x1 = x1, x0
    if y1 < y0:
        y0, y1 = y1, y0
    for y in range(y0, y1 + 1):
        dda(pixels, x0, y, x1, y, color, ancho, alto)


def rellenar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Rellena un triangulo horizontalmente: en cada fila se calcula el
    intervalo [x_izq, x_der] y se traza con dda()."""
    ys = [p1[1], p2[1], p3[1]]
    for y in range(min(ys), max(ys) + 1):
        cruces = []
        for (ax, ay), (bx, by) in ((p1, p2), (p2, p3), (p3, p1)):
            if ay == by:
                continue
            if min(ay, by) <= y <= max(ay, by):
                t = (y - ay) / (by - ay)
                cruces.append(ax + (bx - ax) * t)
        if len(cruces) >= 2:
            dda(pixels, int(min(cruces)), y, int(max(cruces)), y, color,
                ancho, alto)


def rellenar_triangulo_degradado(pixels, p1, p2, p3, color_a, color_b,
                                  ancho, alto):
    """Rellena un triangulo fila por fila con un gradiente vertical de color
    (extension voluntaria). El color se interpola segun la altura (y)."""
    y_min = min(p1[1], p2[1], p3[1])
    y_max = max(p1[1], p2[1], p3[1])
    for y in range(y_min, y_max + 1):
        cruces = []
        for (ax, ay), (bx, by) in ((p1, p2), (p2, p3), (p3, p1)):
            if ay == by:
                continue
            if min(ay, by) <= y <= max(ay, by):
                t = (y - ay) / (by - ay)
                cruces.append(ax + (bx - ax) * t)
        if len(cruces) >= 2:
            t = 0.0 if y_max == y_min else (y - y_min) / (y_max - y_min)
            color = interpolar_color(color_a, color_b, t)
            dda(pixels, int(min(cruces)), y, int(max(cruces)), y, color,
                ancho, alto)


def rellenar_circulo(pixels, cx, cy, radio, color, ancho, alto):
    """Rellena un circulo con lineas horizontales trazadas con dda():
    en cada fila se calcula la mitad del ancho de la circunferencia."""
    for dy in range(-radio, radio + 1):
        medio = int(math.sqrt(max(0.0, radio * radio - dy * dy)))
        dda(pixels, cx - medio, cy + dy, cx + medio, cy + dy, color,
            ancho, alto)


def dibujar_poligono(pixels, vertices, color, ancho, alto, cerrar=True):
    """Poligono cualquiera: una llamada a dda() por cada lado."""
    for i in range(len(vertices) - 1):
        dda(pixels, vertices[i][0], vertices[i][1],
            vertices[i + 1][0], vertices[i + 1][1], color, ancho, alto)
    if cerrar:
        dda(pixels, vertices[-1][0], vertices[-1][1],
            vertices[0][0], vertices[0][1], color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Sol: circunferencia de lados + n_rayos que irradian del punto central.

    El angulo de cada rayo se calcula en coordenadas polares (seno y coseno).
    """
    # Circulo del sol usando poligono inscrito de 24 lados.
    rellenar_circulo(pixels, cx, cy, radio, color, ancho, alto)
    circulo = []
    lados = 24
    for i in range(lados):
        angulo = 2 * math.pi * i / lados
        circulo.append((cx + int(radio * math.cos(angulo)),
                         cy + int(radio * math.sin(angulo))))
    dibujar_poligono(pixels, circulo, color, ancho, alto)

    # Rayos: partiendo del borde del circulo hacia afuera.
    largo = radio * 1.6
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos
        xa = cx + int((radio + 4) * math.cos(angulo))
        ya = cy + int((radio + 4) * math.sin(angulo))
        xb = cx + int(largo * math.cos(angulo))
        yb = cy + int(largo * math.sin(angulo))
        dda(pixels, xa, ya, xb, yb, color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Puerta rectangular: relleno + 4 lineas del marco + tirador."""
    rellenar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    dibujar_rectangulo(pixels, x0, y0, x1, y1, (72, 46, 26), ancho, alto)
    # Travesanos del marco (2 lineas) y tirador de color claro.
    dda(pixels, x0 + 8, (y0 + y1) // 2, x1 - 8, (y0 + y1) // 2,
        (72, 46, 26), ancho, alto)
    dda(pixels, (x0 + x1) // 2, y0 + 10, (x0 + x1) // 2, y1 - 10,
        (72, 46, 26), ancho, alto)
    dda(pixels, x1 - 12, (y0 + y1) // 2 - 12, x1 - 8, (y0 + y1) // 2 - 8,
        (250, 220, 120), ancho, alto)
    dda(pixels, x1 - 12, (y0 + y1) // 2 + 8, x1 - 8, (y0 + y1) // 2 + 12,
        (250, 220, 120), ancho, alto)


def dibujar_ventana(pixels, x0, y0, x1, y1, color, ancho, alto, color_marco):
    """Ventana cuadrada: relleno del vidrio + 4 lineas del marco +
    travesanhos (2 lineas)."""
    rellenar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color_marco, ancho, alto)
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    dda(pixels, cx, y0, cx, y1, color_marco, ancho, alto)   # travesano vertical
    dda(pixels, x0, cy, x1, cy, color_marco, ancho, alto)   # travesano horizontal


def dibujar_linea_piso(pixels, x_ini, x_fin, y, color, ancho, alto):
    """Linea de piso horizontal que atraviesa toda la imagen."""
    dda(pixels, x_ini, y, x_fin, y, color, ancho, alto)


def dibujar_arbol(pixels, x, y_base, alto_tronco, color_tronco, color_copa,
                   ancho, alto):
    """Arbol: tronco rectangular + copa triangular (extension voluntaria)."""
    mitad = 8
    punta = (x, y_base - alto_tronco - 55)
    base_izq = (x - 28, y_base - alto_tronco)
    base_der = (x + 28, y_base - alto_tronco)
    # Copa: relleno y luego sus 3 lineas.
    rellenar_triangulo(pixels, punta, base_der, base_izq, color_copa, ancho, alto)
    dibujar_triangulo(pixels, punta, base_der, base_izq, (28, 82, 38), ancho, alto)
    # Tronco: relleno y sus 4 lineas.
    rellenar_rectangulo(pixels, x - mitad, y_base - alto_tronco,
                         x + mitad, y_base, color_tronco, ancho, alto)
    dibujar_rectangulo(pixels, x - mitad, y_base - alto_tronco,
                       x + mitad, y_base, (78, 48, 26), ancho, alto)


def dibujar_nube(pixels, cx, cy, escala, color, ancho, alto):
    """Nube formada por varias lineas cortas (extension voluntaria)."""
    # Cada grupo de 3 lineas forma un "borde" redondeado de la nube.
    partes = [(-45, 0, 25), (-20, -18, 32), (12, -10, 28), (40, 4, 22)]
    for dx, dy, largo in partes:
        x0 = cx + int(dx * escala)
        y0 = cy + int(dy * escala)
        dda(pixels, x0, y0, x0 + int(largo * escala / 2), y0,
            color, ancho, alto)
        dda(pixels, x0 + int(largo * escala / 2), y0, x0 + int(largo * escala),
            y0 + int(dy * escala / 2), color, ancho, alto)
        dda(pixels, x0 + int(largo * escala), y0 + int(dy * escala / 2),
            x0 + int(largo * escala), y0 + int(largo * escala / 3),
            color, ancho, alto)
    # Base de la nube.
    dda(pixels, cx - 45 * escala, cy + 8 * escala,
        cx + 60 * escala, cy + 8 * escala, color, ancho, alto)


def dibujar_humo(pixels, x, y, color, ancho, alto, n_umas=4):
    """Humo saliendo de la chimenea: pequenas lineas que suben en zigzag."""
    for i in range(n_umas):
        y0 = y - i * 14
        x0 = x + (6 if i % 2 == 0 else -6)
        dda(pixels, x0, y0, x0 + 10, y0 - 12, color, ancho, alto)
        dda(pixels, x0 + 10, y0 - 12, x0 - 4, y0 - 22, color, ancho, alto)


def dibujar_suelo_degradado(pixels, y_ini, y_fin, color_a, color_b,
                            ancho, alto):
    """Cesped con gradiente de color (extension voluntaria): se traza una
    linea horizontal con dda() por cada fila, interpolando el color."""
    if y_fin == y_ini:
        return
    for y in range(y_ini, y_fin + 1):
        color = interpolar_color(color_a, color_b, (y - y_ini) / (y_fin - y_ini))
        dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


# ---------------------------------------------------------------------------
# 4. Programa principal
# ---------------------------------------------------------------------------
def main():
    ancho, alto = 600, 500

    # Lienzo: se inicializa con el color del cielo.
    imagen = Image.new("RGB", (ancho, alto), (198, 226, 255))
    pixels = imagen.load()

    # Paleta de la composicion (cada elemento usa un color distinto).
    COLOR_TECHO_A = (196, 62, 46)
    COLOR_TECHO_B = (128, 34, 26)
    COLOR_PARED = (222, 184, 135)
    COLOR_PUERTA = (110, 74, 44)
    COLOR_VENTANA = (168, 226, 246)
    COLOR_MARCO = (240, 248, 255)
    COLOR_PISO = (94, 68, 44)
    COLOR_SOL = (250, 196, 42)
    COLOR_TRONCO = (122, 78, 42)
    COLOR_COPA = (52, 122, 58)
    COLOR_NUBE = (255, 255, 255)
    COLOR_HUMO = (188, 196, 205)
    COLOR_CESped_A = (118, 178, 82)
    COLOR_CESped_B = (62, 122, 54)

    # --- Fondo: sol en la esquina superior derecha (12 rayos) ---
    dibujar_sol(pixels, 505, 72, 34, 12, COLOR_SOL, ancho, alto)

    # --- Fondo: dos nubes ---
    dibujar_nube(pixels, 150, 70, 1.0, COLOR_NUBE, ancho, alto)
    dibujar_nube(pixels, 340, 105, 0.75, COLOR_NUBE, ancho, alto)

    # --- Suelo con gradiente y linea de piso ---
    dibujar_suelo_degradado(pixels, 430, alto - 1, COLOR_CESped_A,
                            COLOR_CESped_B, ancho, alto)
    dibujar_linea_piso(pixels, 0, ancho - 1, 430, COLOR_PISO, ancho, alto)

    # --- Arboles del paisaje (extension) ---
    dibujar_arbol(pixels, 95, 430, 42, COLOR_TRONCO, COLOR_COPA, ancho, alto)
    dibujar_arbol(pixels, 530, 430, 34, COLOR_TRONCO, COLOR_COPA, ancho, alto)

    # --- 1) Cuerpo de la casa: rectangulo (4 lineas) ---
    rellenar_rectangulo(pixels, 180, 260, 430, 430, (243, 220, 191), ancho, alto)
    dibujar_rectangulo(pixels, 180, 260, 430, 430, COLOR_PARED, ancho, alto)

    # --- 2) Techo: triangulo (3 lineas) con gradiente ---
    p_izq = (158, 260)
    p_punta = (305, 140)
    p_der = (452, 260)
    rellenar_triangulo_degradado(pixels, p_punta, p_der, p_izq, COLOR_TECHO_A,
                                  COLOR_TECHO_B, ancho, alto)
    dibujar_linea_degradada(pixels, p_izq[0], p_izq[1], p_punta[0], p_punta[1],
                            COLOR_TECHO_A, COLOR_TECHO_B, ancho, alto, tramos=40)
    dibujar_linea_degradada(pixels, p_punta[0], p_punta[1], p_der[0], p_der[1],
                            COLOR_TECHO_B, COLOR_TECHO_A, ancho, alto, tramos=40)
    dda(pixels, p_izq[0], p_izq[1], p_der[0], p_der[1], COLOR_TECHO_B,
        ancho, alto)

    # Chimenea y humo (extension).
    dda(pixels, 390, 175, 420, 175, COLOR_TECHO_B, ancho, alto)
    dda(pixels, 420, 175, 420, 235, COLOR_TECHO_B, ancho, alto)
    dda(pixels, 420, 235, 390, 235, COLOR_TECHO_B, ancho, alto)
    dda(pixels, 390, 235, 390, 175, COLOR_TECHO_B, ancho, alto)
    dibujar_humo(pixels, 405, 172, COLOR_HUMO, ancho, alto)

    # --- 3) Puerta rectangular (4 lineas) ---
    dibujar_puerta(pixels, 275, 350, 335, 430, COLOR_PUERTA, ancho, alto)

    # --- 4) Dos ventanas cuadradas (4 lineas cada una) ---
    dibujar_ventana(pixels, 205, 300, 255, 350, COLOR_VENTANA,
                    ancho, alto, COLOR_MARCO)
    dibujar_ventana(pixels, 355, 300, 405, 350, COLOR_VENTANA,
                    ancho, alto, COLOR_MARCO)

    # Guarda la imagen resultante.
    imagen.save("casa.png")
    print("casa.png generada correctamente (600 x 500 px)")


if __name__ == "__main__":
    main()