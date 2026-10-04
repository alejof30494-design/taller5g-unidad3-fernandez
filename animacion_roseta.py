# -*- coding: utf-8 -*-
"""
Extension voluntaria - Animacion de rosetas (GIF)
Tarea practica Unidad III - Conversion por rastreo
Universidad Americana - Taller de Programacion de 5.a Generacion I

Genera 20 rosetas con N creciente (de 5 a 24) y las combina en un GIF animado.
Reutiliza las funciones bresenham(), generar_puntos_circulo() y dibujar_roseta()
del ejercicio 2.

Salida: rosetas_animacion.gif
"""

from PIL import Image
import math

# Se importan las funciones ya implementadas para no duplicar el codigo.
from ejercicio2_roseta import bresenham, generar_puntos_circulo, dibujar_roseta


ANCHO = ALTO = 400
CENTRO = (200, 200)
RADIO = 170
N_FRAMAS = 20          # de 5 a 24 puntos
N_INICIAL = 5
FONDO = "white"


def main():
    imagenes = []

    for k in range(N_FRAMAS):
        n = N_INICIAL + k
        imagen = Image.new("RGB", (ANCHO, ALTO), FONDO)
        pixels = imagen.load()
        puntos = generar_puntos_circulo(CENTRO[0], CENTRO[1], RADIO, n)
        dibujar_roseta(pixels, puntos, ANCHO, ALTO)
        imagenes.append(imagen)
        print(f"fotograma {k + 1}/{N_FRAMAS} listo (N = {n})")

    # Guardado del GIF: 120 ms por fotograma y repeticion infinita.
    imagenes[0].save(
        "rosetas_animacion.gif",
        save_all=True,
        append_images=imagenes[1:],
        duration=120,
        loop=0,
    )
    print("rosetas_animacion.gif generada correctamente "
          f"({N_FRAMAS} fotogramas, N de {N_INICIAL} a {N_INICIAL + N_FRAMAS - 1})")


if __name__ == "__main__":
    main()