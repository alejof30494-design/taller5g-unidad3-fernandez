# Taller 5G · Unidad III — Conversión por rastreo (DDA y Bresenham)

Tarea práctica de la asignatura **Taller de Programación de 5.ª Generación I**
(Facultad de Ciencias y Tecnología, Universidad Americana).
Docente: Prof. Mgtr. Alberto F. Giménez Méndez.

- Alumno: **Alejo Fernandez**
- Matrícula: **5181387**
- Correo institucional de referencia: `alejof30494-design`
- Repositorio: https://github.com/alejof30494-design/taller5g-unidad3-fernandez
- Año: Asunción, Paraguay · 2026

---

## Contenido del repositorio

| Archivo | Descripción |
|---|---|
| `ejercicio1_casa.py` | Ejercicio 1: casa estilizada trazada con `dda()`. Genera `casa.png` (600 × 500). |
| `ejercicio2_roseta.py` | Ejercicio 2: rosetas geométricas trazadas con `bresenham()`. Genera `roseta_12.png`, `roseta_24.png`, `roseta_36.png` (700 × 700) y las extensiones `roseta_salto5.png`, `roseta_salto7.png`. |
| `animacion_roseta.py` | Extensión voluntaria: 20 rosetas con N creciente (5 a 24) combinadas en `rosetas_animacion.gif`. |
| `casa.png` | Imagen de salida del Ejercicio 1. |
| `roseta_12.png`, `roseta_24.png`, `roseta_36.png` | Imágenes de salida del Ejercicio 2. |
| `roseta_salto5.png`, `roseta_salto7.png` | Rosetas estrelladas (conexión de puntos no adyacentes). |
| `rosetas_animacion.gif` | Animación de rosetas. |

## Requisitos

- Python 3.8 o superior.
- Pillow:

```bash
pip install Pillow
```

## Cómo ejecutar

```bash
python ejercicio1_casa.py       # genera casa.png
python ejercicio2_roseta.py     # genera roseta_12.png, roseta_24.png, roseta_36.png, roseta_salto5.png, roseta_salto7.png
python animacion_roseta.py      # genera rosetas_animacion.gif
```

Las imágenes se guardan en la misma carpeta desde donde se ejecuta el script.

---

## Ejercicio 1 — Composición geométrica con DDA

**Estrategia.** Se implementó `dda(pixels, x0, y0, x1, y1, color, ancho, alto)`
con la misma firma usada en clase: se calcula el número de pasos como la
proyección del segmento sobre el eje de mayor desplazamiento y se redondea la
coordenada en cada paso (regla del pixel dominante), con recorte contra los
bordes del frame buffer.

Sobre esa función se construyeron primitivas independientes —una por elemento
gráfico— y todas las llamadas terminan finalmente en `dda()`:

- `dibujar_rectangulo` (cuerpo de la casa, 4 líneas).
- `dibujar_triangulo` (techo, 3 líneas).
- `dibujar_puerta` (4 líneas del marco + travesaños).
- `dibujar_ventana` (4 líneas por ventana, 8 en total).
- `dibujar_sol` (polígono inscrito de 24 lados + 12 rayos calculados con
  seno y coseno).
- `dibujar_linea_piso` (línea horizontal de 0 a 599 px).

Cada elemento tiene un color distinto (techo, paredes, puerta, vidrio y marco de
las ventanas, sol, piso, árboles y nubes).

**Extensiones voluntarias incluidas:** árboles (tronco rectangular + copa
triangular), dos nubes formadas por líneas cortas, humo saliendo de la chimenea
y gradientes de color (techo con degradado vertical, línea de techo con
degradado lateral y césped con degradado). Los rellenos (paredes, puerta,
vidrio, copa de los árboles, disco del sol) también se realizan con `dda()`,
usando líneas horizontales fila por fila.

## Ejercicio 2 — Composición dinámica con Bresenham

**Estrategia.** `bresenham(pixels, x0, y0, x1, y1, color, ancho, alto)` se
implementa con aritmética entera: `dx = |x1-x0|`, `dy = -|y1-y0|`, error
inicial `err = dx + dy` y la regla `e2 = 2*err` para decidir el paso en X y/o
en Y, con las variables de sentido `sx` y `sy` para líneas con coordenadas
decrecientes.

`generar_puntos_circulo(cx, cy, radio, n)` distribuye los n puntos
equiespaciados usando `2*pi*i/n` con `math.cos` y `math.sin`.
`dibujar_roseta(pixels, puntos, ancho, alto)` recorre todos los pares de
puntos (N=24 → 276 líneas) y calcula el color de cada línea a partir del punto
medio de la cuerda: el **matiz** se obtiene del ángulo respecto del centro
(HSV recorre todo el espectro) y la **luminosidad** de la distancia normalizada
al centro, lo que produce el gradiente radial.

**Extensiones voluntarias incluidas:** rosetas estrelladas que conectan solo
puntos no adyacentes (`salto = 5` y `salto = 7`) y la animación en GIF con
20 rosetas de N creciente.

---

## Publicación en Git

```bash
cd taller5g-unidad3-fernandez
git init
git add .
git commit -m "Entrega tarea Unidad III"
git branch -M main
git remote add origin https://github.com/alejof30494-design/taller5g-unidad3-fernandez.git
git push -u origin main
```

> Si el repositorio es privado, hay que agregar al docente
> (`alberto-gimenez`) como colaborador e indicarlo en el documento de entrega.