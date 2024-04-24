from PIL import Image, ImageDraw
import random

# Dimensiones de la imagen y de la matriz
ancho = 600
altura = 900
filas = 50
columnas = 24

# Tamaño de cada cuadrado
tamano_textura = ancho // columnas

# Paletas de colores
paletas = [
    [(245, 245, 220), (210, 180, 140), (160, 82, 45), (139, 69, 19)],  # Paleta de tonos tierra
    [(255, 255, 255), (0, 0, 255), (255, 0, 0), (255, 255, 0)],        # Paleta de colores primarios
    [(128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 69, 0)],       # Paleta de colores vivos
    [(173, 216, 230), (25, 25, 112),(64, 224, 208),(127, 255, 212)],   # Paleta de colores marinos
    [(255, 0, 0),(255, 165, 0),(255, 255, 0),(128, 30, 0)],            # Paleta de colores fuego
    [(139, 0, 0),(255, 0, 0),(255, 99, 71),(165, 42, 42)],             # Paleta de colores sangrientos
    [(152, 255, 152),(50, 205, 50),(0, 128, 0),(144, 238, 144)],       # Paleta de colores menta
    [(255, 0, 255),(128, 20, 150),(250, 215, 0),(250, 250, 250)]       # Paleta de colores de lujo
]

# Crear una nueva matriz para representar los colores de los cuadrados
matriz_color = [[(255, 255, 255) for _ in range(columnas)] for _ in range(filas)]

# Función para generar una imagen de forma procedural con reglas utilizando una matriz
def generacion_procedural(matriz_color):
    # Seleccionar una paleta aleatoria
    paleta = random.choice(paletas)

    # Iterar sobre las filas y columnas de la matriz
    for i in range(filas):
        for j in range(columnas):
            # Seleccionar un color aleatorio de la paleta
            color = random.choice(paleta)
            # Actualizar el color en la matriz
            matriz_color[i][j] = color

# Generar la matriz de colores de forma procedural
generacion_procedural(matriz_color)

# Crear una nueva imagen en blanco
imagen = Image.new("RGB", (ancho, altura), "white")

# Crear un objeto ImageDraw para dibujar en la imagen
draw = ImageDraw.Draw(imagen)

# Dibujar los cuadrados utilizando los colores de la matriz
for i in range(filas):
    for j in range(columnas):
        # Obtener el color de la matriz
        color = matriz_color[i][j]
        # Calcular las coordenadas del cuadrado
        x0 = j * tamano_textura
        y0 = i * tamano_textura
        x1 = x0 + tamano_textura
        y1 = y0 + tamano_textura
        # Dibujar el cuadrado
        draw.rectangle([(x0, y0), (x1, y1)], fill=color)

# Guardar la imagen generada
imagen.save("Textura.png")

# Mostrar la imagen generada
imagen.show()
