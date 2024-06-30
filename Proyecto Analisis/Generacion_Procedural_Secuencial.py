from PIL import Image, ImageDraw
import random
import cv2
import numpy as np
import concurrent.futures

#Definición de funciones:

def diferencia_de_color(color1, color2):
    # Calcula la diferencia total de color entre dos colores RGB
    r_diff = abs(color1[0] - color2[0])
    g_diff = abs(color1[1] - color2[1])
    b_diff = abs(color1[2] - color2[2])
    return r_diff + g_diff + b_diff

def generar_color_con_restriccion(color_base, paletas, diferencia_minima):
    # Genera un color aleatorio dentro de una cierta diferencia mínima de color de color_base
    while True:
        nuevo_color = random.choice(random.choice(paletas))
        if diferencia_de_color(color_base, nuevo_color) >= diferencia_minima:
            return nuevo_color

# Función para generar una imagen de forma procedural con reglas utilizando una matriz
def generacion_procedural(matriz_blanca, paletas, diferencia_minima):
    # Seleccionar una paleta aleatoria
    paleta = random.choice(paletas)
    # Generar un color base aleatorio
    color_base = random.choice(paleta)
    for i in range(filas):
        for j in range(columnas):
            # Seleccionar un color aleatorio de la paleta
            color_restringido = generar_color_con_restriccion(color_base, paletas, diferencia_minima)
            # Actualizar el color en la matriz
            matriz_blanca[i][j] = color_restringido
        
# Empezamos con las estadísticas
# AF: Ataque físico
# AM: Ataque mágico
# VA: Velocidad de ataque
# RV: Robo de vida
# Dur: Durabilidad
# PC: Probabilidad de crítico
# DC: Daño crítico
def estadisticas(nivel):
    af = random.randint(nivel * 1, nivel * 5)
    am = random.randint(nivel * 1, nivel * 5)
    va = random.randint(nivel * 1, nivel * 5)
    rv = random.randint(nivel * 1, nivel * 5)
    dur = random.randint(1, 100)
    pc = random.randint(1, 100)
    dc = random.randint(1, 100)
    efecto = generar_efecto()
    arma = [af, am, va, rv, dur, pc, dc, efecto]
    return arma

def generar_efecto():
    efecto = random.choice(["Fuego", "Hielo", "Veneno", "Luz", "Oscuridad", "Aturdimiento", "Looteo"])
    return efecto

def generar_arma(nivel):
    arma = estadisticas(nivel)
    
    prob = random.randint(1, 100)
    if prob <= 10:
        efecto2 = generar_efecto()
        arma.append(efecto2)
    else:
        arma.append("   ")
    
    if prob == 1:
        efecto3 = generar_efecto()
        arma.append(efecto3)
    else:
        arma.append("   ")
    return arma

# Termino de la definición de funciones.

# Dimensiones de la imagen y de la matriz
ancho = 720
altura = 1280
filas = 64
columnas = 36
tamano_textura = ancho // columnas # Tamaño de cada cuadrado

# Paletas de colores del filo y del mango
paletas_filos = [
    [(245, 245, 220), (210, 180, 140), (160, 82, 45), (139, 69, 19)],  # Paleta de tonos tierra
    [(255, 255, 255), (0, 0, 255), (255, 0, 0), (255, 255, 0)],        # Paleta de colores primarios
    [(128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 69, 0)],       # Paleta de colores vivos
    [(173, 216, 230), (25, 25, 112), (64, 224, 208), (127, 255, 212)], # Paleta de colores marinos
    [(255, 0, 0), (255, 165, 0), (255, 255, 0), (128, 30, 0)],         # Paleta de colores fuego
    [(139, 0, 0), (255, 0, 0), (255, 99, 71), (165, 42, 42)],          # Paleta de colores sangrientos
    [(152, 255, 152), (50, 205, 50), (0, 128, 0), (144, 238, 144)],    # Paleta de colores menta
    [(255, 0, 255), (128, 20, 150), (250, 215, 0), (250, 250, 250)]    # Paleta de colores de lujo
]
paletas_mangos = [
    [(245, 245, 220), (210, 180, 140), (160, 82, 45), (139, 69, 19)],     # Paleta de tonos tierra
    [(128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 69, 0)],          # Paleta de colores vivos
    [(139, 69, 19), (139, 90, 43), (222, 184, 135), (205, 133, 63)],      # Tonos de madera
    [(192, 192, 192), (128, 128, 128), (169, 169, 169), (105, 105, 105)]  # Tonos de metal
]
# Se crea la nueva matriz para representar los colores de los cuadrados
matriz_blanca_filo = [[(0, 0, 0) for _ in range(columnas)] for _ in range(filas)]
matriz_blanca_mango = [[(0, 0, 0) for _ in range(columnas)] for _ in range(filas)]

# Generar la matriz de colores de forma procedural
generacion_procedural(matriz_blanca_filo, paletas_filos, 400)
generacion_procedural(matriz_blanca_mango, paletas_mangos, 200)

# Crear una nueva imagen en blanco
imagen_filo = Image.new("RGB", (ancho, altura), "black")
imagen_mango = Image.new("RGB", (ancho, altura), "black")

# Crear un objeto ImageDraw para dibujar en la imagen
draw_filo = ImageDraw.Draw(imagen_filo)
draw_mango = ImageDraw.Draw(imagen_mango)

# Dibujar los cuadrados utilizando los colores de la matriz
for i in range(filas):
    for j in range(columnas):
        # Obtener el color de la matriz
        color_filo = matriz_blanca_filo[i][j]
        color_mango = matriz_blanca_mango[i][j]
        # Calcular las coordenadas del cuadrado
        # Para el filo:
        f_x0 = j * tamano_textura
        f_y0 = i * tamano_textura
        f_x1 = f_x0 + tamano_textura
        f_y1 = f_y0 + tamano_textura
        # Para el mango:
        m_x0 = j * tamano_textura
        m_y0 = i * tamano_textura
        m_x1 = m_x0 + tamano_textura
        m_y1 = m_y0 + tamano_textura
        # Dibujar el cuadrado
        draw_filo.rectangle([(f_x0, f_y0), (f_x1, f_y1)], fill=color_filo)
        draw_mango.rectangle([(m_x0, m_y0), (m_x1, m_y1)], fill=color_mango)

# Guardar la imagen generada
imagen_filo.save("Textura.png")
imagen_mango.save("Textura_Mango.png")

# Cargar la imagen generada con cv2
imagen_filo = cv2.imread('Textura.png')
imagen_mango = cv2.imread('Textura_Mango.png')

#Seleccionar el tipo de arma
tipo = random.choice([0,1,2]) # 0 para espada, 1 para hacha, 2 para lanza.

if (tipo == 0):
    # Definir los puntos en donde se podrá ensamblar el filo con el mango
    punto_der_ensamble = random.randint(350, 450)
    punto_izq_ensamble = random.randint(150, 250)

    # Definir los puntos que definiran los bordes del mango
    puntos_mango = np.array([
        [punto_izq_ensamble, 800],
        [punto_izq_ensamble - random.randint(0, 15), random.randint(795, 820)],
        [punto_izq_ensamble - random.randint(0, 15), random.randint(820, 880)],
        [random.randint(250, 290), random.randint(820, 880)],
        [random.randint(270, 295), random.randint(900, 1100)],
        [random.randint(305, 325), random.randint(900, 1100)],
        [random.randint(310, 350), random.randint(820, 880)],
        [punto_der_ensamble + random.randint(0, 15), random.randint(820, 880)],
        [punto_der_ensamble + random.randint(0, 15), 800],
        [punto_der_ensamble, 800]
    ], np.int32)

    # Definir los puntos que definiran los bordes del filo
    puntos_filo = np.array([
        [punto_der_ensamble, 800],
        [random.randint(350, 450), random.randint(750, 780)],
        [random.randint(350, 450), random.randint(550, 650)],
        [random.randint(350, 450), random.randint(350, 450)],
        [random.randint(350, 450), random.randint(150, 250)],
        [random.randint(150, 300), random.randint(50, 150)],
        [random.randint(150, 250), random.randint(150, 250)],
        [random.randint(150, 250), random.randint(450, 550)],
        [random.randint(150, 250), random.randint(650, 750)],
        [punto_izq_ensamble, 800]
    ], np.int32)

    # Definir las coordenadas de inicio y fin de la línea
    # Para separar el mango del filo
    x1, y1 = punto_der_ensamble, 800
    x2, y2 = punto_izq_ensamble, 800

elif(tipo == 1):
    # Definir los puntos en donde se podrá ensamblar el filo con el mango
    punto_der_ensamble = random.randint(390, 430)
    punto_izq_ensamble = random.randint(350, 370)
    # Definir los puntos que definiran los bordes del mango
    puntos_mango = np.array([
        [punto_izq_ensamble, 500],
        [punto_izq_ensamble - random.randint(0, 15), 900],
        [punto_der_ensamble + random.randint(0, 15), 900],
        [punto_der_ensamble, 500]
    ], np.int32)

    # Definir los puntos que definiran los bordes del filo
    puntos_filo = np.array([
        [punto_izq_ensamble, 500],
        [punto_izq_ensamble - random.randint(0, 50), random.randint(460, 480)],
        [punto_izq_ensamble - random.randint(50, 100), 500],
        [punto_izq_ensamble - random.randint(100, 150), 550],
        [punto_izq_ensamble - random.randint(150, 250), 400],
        [punto_izq_ensamble - random.randint(100, 150), 300],
        [punto_izq_ensamble - random.randint(50, 100), 250],
        [punto_izq_ensamble - random.randint(0, 50), random.randint(330, 350)],
        [punto_izq_ensamble, 300],
        [punto_der_ensamble, 300],
        [punto_der_ensamble + random.randint(0, 50), random.randint(330, 350)],
        [punto_der_ensamble + random.randint(50, 100), 270],
        [punto_der_ensamble + random.randint(100, 150), 250],
        [punto_der_ensamble + random.randint(150, 250), 400],
        [punto_der_ensamble + random.randint(100, 150), 550],
        [punto_der_ensamble + random.randint(50, 100), 520],
        [punto_der_ensamble + random.randint(0, 50), random.randint(460, 480)],
        [punto_der_ensamble, 500]
    ], np.int32)

    # Definir las coordenadas de inicio y fin de la línea
    # Para separar el mango del filo
    x1, y1 = punto_der_ensamble, 500
    x2, y2 = punto_izq_ensamble, 500

elif(tipo == 2):
    # Definir los puntos en donde se podrá ensamblar el filo con el mango
    punto_der_ensamble = random.randint(390, 430)
    punto_izq_ensamble = random.randint(350, 370)
    # Definir los puntos que definiran los bordes del mango
    puntos_mango = np.array([
        [punto_izq_ensamble, 350],
        [punto_izq_ensamble - random.randint(0, 15), 1000],
        [punto_der_ensamble + random.randint(0, 15), 1000],
        [punto_der_ensamble, 350]
    ], np.int32)

    # Definir los puntos que definiran los bordes del filo
    puntos_filo = np.array([
        [punto_izq_ensamble, 350],
        [punto_izq_ensamble - random.randint(0, 50), 250],
        [punto_izq_ensamble - random.randint(0, 50), 200],
        [punto_izq_ensamble + random.randint(0, 50) , random.randint(50, 150)],
        [punto_der_ensamble + random.randint(0, 50), 200],
        [punto_der_ensamble + random.randint(0, 50), 250],
        [punto_der_ensamble, 350]
    ], np.int32)

    # Definir las coordenadas de inicio y fin de la línea
    # Para separar el mango del filo
    x1, y1 = punto_der_ensamble, 350
    x2, y2 = punto_izq_ensamble, 350


# Crear una máscara en blanco con el mismo tamaño que la imagen
mascara_filo = np.zeros_like(imagen_filo)
mascara_mango = np.zeros_like(imagen_mango)

# Dibujar la forma de la espada en la máscara
cv2.fillPoly(mascara_filo, [puntos_filo], (255, 255, 255))
cv2.fillPoly(mascara_mango, [puntos_mango], (255, 255, 255))

# Aplicar la máscara a la imagen para recortarla
imagen_filo_recortada = cv2.bitwise_and(imagen_filo, mascara_filo)
imagen_mango_recortada = cv2.bitwise_and(imagen_mango, mascara_mango)

# Superponer la imagen del filo sobre la del mango
arma = cv2.addWeighted(imagen_filo_recortada, 1, imagen_mango_recortada, 1, 0)

# Dibujar la línea negra en la imagen para separar
# el filo del mango
grosor = 1
arma = cv2.line(arma, (x1, y1), (x2, y2), (0, 0, 0), grosor)

# Guardar la imagen en el archivo "Arma.png"
cv2.imwrite("Arma.png", arma)

# Mostrar la imagen superpuesta
cv2.imshow('Arma', arma)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Nivel del jugador (constante para esta prueba)
nivel = 13
arma = generar_arma(nivel)
datos_arma = ["Ataque fisico", "Ataque magico", "Velocidad de ataque", "Robo de vida", "Durabilidad",
               "Probabilidad de critico", "Dano critico", "Efecto/s", "    ", "    "]
datos_finales = np.array([datos_arma, arma]).T
# Se guardan las estadisticas del arma en un archivo
with open("archivo.txt", "w") as archivo:
    for fila in datos_finales:
        fila_str = " ".join(map(str, fila))
        archivo.write(fila_str + "\n")
        