# -*- coding: utf-8 -*-
"""
Ejercicio 2 - Composicion dinamica con Bresenham (roseta geometrica)
Tarea practica Unidad III - Conversion por rastreo
Universidad Americana - Taller de Programacion de 5.a Generacion I

Genera rosetas trazando lineas entre pares de puntos equiespaciados sobre una
circunferencia imaginaria, usando la funcion bresenham() sin modificar su
firma. El color de cada linea depende del angulo y de la distancia de la
linea respecto del centro (gradiente).

Salidas: roseta_12.png, roseta_24.png, roseta_36.png
          roseta_salto5.png y roseta_salto7.png (extension voluntaria)
"""

from PIL import Image
import math
import colorsys


# ---------------------------------------------------------------------------
# 1. Algoritmo de Bresenham (linea entera, solo operaciones enteras)
# ---------------------------------------------------------------------------
# Reutiliza la funcion tal como fue presentada en clase, sin modificar su
# firma: bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)
#
# Se elige el "pixel dominante" (el eje con mayor desplazamiento) y se
# mantiene un error acumulado que se va actualizando en cada paso, de modo que
# solo hay que decidir si el pixel siguiente se desplaza en X, en Y o en ambos.
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una recta entre (x0,y0) y (x1,y1) con el algoritmo de Bresenham."""
    x0 = int(round(x0))
    y0 = int(round(y0))
    x1 = int(round(x1))
    y1 = int(round(y1))

    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)

    # Sentido del avance en cada eje (para lineas con coordenadas decrecientes).
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    # Error inicial: dx + dy.
    err = dx + dy

    while True:
        # Escribe el pixel actual (con recorte contra los bordes del lienzo).
        if 0 <= x0 < ancho and 0 <= y0 < alto:
            pixels[x0, y0] = color

        if x0 == x1 and y0 == y1:
            break

        e2 = 2 * err
        if e2 >= dy:            # paso en X
            err += dy
            x0 += sx
        if e2 <= dx:            # paso en Y
            err += dx
            y0 += sy


# ---------------------------------------------------------------------------
# 2. Distribucion de puntos sobre la circunferencia
# ---------------------------------------------------------------------------
def generar_puntos_circulo(cx, cy, radio, n):
    """Devuelve una lista de n puntos equiespaciados sobre la circunferencia
    de centro (cx, cy) y radio 'radio', usando coseno y seno."""
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(radio * math.cos(angulo))
        y = cy + int(radio * math.sin(angulo))
        puntos.append((x, y))
    return puntos


# ---------------------------------------------------------------------------
# 3. Gradiente de color
# ---------------------------------------------------------------------------
def color_gradiente(angulo, distancia, radio_maximo):
    """Devuelve el color RGB de una linea a partir de su angulo respecto del
    centro y de su distancia normalizada (0 = cerca del centro, 1 = borde).

    - El matiz (hue) recorre todo el espectro segun el angulo de la linea.
    - La luminosidad aumenta con la distancia: el centro queda mas oscuro y
      el borde mas claro, lo que produce el efecto de relieve radial.
    """
    hue = (angulo / (2 * math.pi)) % 1.0
    t = 0.0 if radio_maximo == 0 else max(0.0, min(1.0, distancia / radio_maximo))
    valor = 0.55 + 0.45 * t          # luminosidad entre 0.55 y 1.0
    saturacion = 0.85
    r, g, b = colorsys.hsv_to_rgb(hue, saturacion, valor)
    return (int(r * 255), int(g * 255), int(b * 255))


# ---------------------------------------------------------------------------
# 4. Trazado de la roseta
# ---------------------------------------------------------------------------
def dibujar_roseta(pixels, puntos, ancho, alto, salto=1, radio_maximo=None):
    """Traza la roseta conectando cada punto con todos los demas mediante
    bresenham(), aplicando el gradiente de color linea por linea.

    'salto' indica cada cuantos puntos se dibuja la conexion: 1 = roseta
    completa (todos los pares), k = solo el poligono estrellado {n/k}.
    """
    n = len(puntos)

    # Centro de la roseta (promedio de los puntos) y radio maximo de referencia
    # para normalizar la distancia en el gradiente de color.
    cx = sum(p[0] for p in puntos) / n
    cy = sum(p[1] for p in puntos) / n
    if radio_maximo is None:
        radio_maximo = max(math.hypot(p[0] - cx, p[1] - cy) for p in puntos)

    for i in range(n):
        for j in range(i + 1, n):
            # En modo estrellado solo se conectan los puntos separados por
            # 'salto' posiciones; en el modo completo, todos los pares.
            if salto > 1:
                distancia = min((j - i) % n, (i - j) % n)
                if distancia != salto:
                    continue

            x0, y0 = puntos[i]
            x1, y1 = puntos[j]

            # Gradiente: se usa el punto medio de la linea (el pie de la
            # perpendicular desde el centro es el punto mas cercano).
            mx = (x0 + x1) / 2.0
            my = (y0 + y1) / 2.0
            angulo = math.atan2(my - cy, mx - cx)
            distancia = math.hypot(mx - cx, my - cy)

            color = color_gradiente(angulo, distancia, radio_maximo)
            bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)


# ---------------------------------------------------------------------------
# 5. Programa principal
# ---------------------------------------------------------------------------
def main():
    ancho = alto = 700
    centro = (350, 350)
    radio = 300
    fondo = "white"          # fondo blanco (la roseta sobre fondo negro tambien
                             # es una opcion valida, ver RUTA_FONDO_NEGRO)

    # Las tres variantes pedidas: N = 12, 24 y 36.
    for n in [12, 24, 36]:
        imagen = Image.new("RGB", (ancho, alto), fondo)
        pixels = imagen.load()
        puntos = generar_puntos_circulo(centro[0], centro[1], radio, n)
        dibujar_roseta(pixels, puntos, ancho, alto)

        lineas = n * (n - 1) // 2
        imagen.save(f"roseta_{n}.png")
        print(f"roseta_{n}.png generada correctamente "
              f"({n} puntos, {lineas} lineas con bresenham)")

    # --- Extension voluntaria: roseta estrellada (solo puntos no adyacentes) ---
    for salto in [5, 7]:
        n = 24
        imagen = Image.new("RGB", (ancho, alto), fondo)
        pixels = imagen.load()
        puntos = generar_puntos_circulo(centro[0], centro[1], radio, n)
        dibujar_roseta(pixels, puntos, ancho, alto, salto=salto)
        imagen.save(f"roseta_salto{salto}.png")
        print(f"roseta_salto{salto}.png generada correctamente "
              f"({n} puntos unidos de a {salto} en {salto})")


if __name__ == "__main__":
    main()