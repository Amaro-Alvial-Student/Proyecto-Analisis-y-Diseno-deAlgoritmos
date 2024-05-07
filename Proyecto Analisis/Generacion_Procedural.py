from PIL import Image, ImageDraw
import random
import cv2
import numpy as np

# Dimensiones de la imagen y de la matriz
ancho = 600
altura = 1200
filas = 50
columnas = 28

# Tamaño de cada cuadrado
tamano_textura = ancho // columnas

# Paletas de colores
paletas_filos = [
    [(245, 245, 220), (210, 180, 140), (160, 82, 45), (139, 69, 19)],  # Paleta de tonos tierra
    [(255, 255, 255), (0, 0, 255), (255, 0, 0), (255, 255, 0)],        # Paleta de colores primarios
    [(128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 69, 0)],       # Paleta de colores vivos
    [(173, 216, 230), (25, 25, 112),(64, 224, 208),(127, 255, 212)],   # Paleta de colores marinos
    [(255, 0, 0),(255, 165, 0),(255, 255, 0),(128, 30, 0)],            # Paleta de colores fuego
    [(139, 0, 0),(255, 0, 0),(255, 99, 71),(165, 42, 42)],             # Paleta de colores sangrientos
    [(152, 255, 152),(50, 205, 50),(0, 128, 0),(144, 238, 144)],       # Paleta de colores menta
    [(255, 0, 255),(128, 20, 150),(250, 215, 0),(250, 250, 250)]       # Paleta de colores de lujo
]

paletas_mangos = [
    [(245, 245, 220), (210, 180, 140), (160, 82, 45), (139, 69, 19)],     # Paleta de tonos tierra
    [(128, 0, 128), (0, 128, 128), (255, 165, 0), (255, 69, 0)],          # Paleta de colores vivos
    [(139, 69, 19), (139, 90, 43), (222, 184, 135), (205, 133, 63)],      # Tonos de madera
    [(192, 192, 192), (128, 128, 128), (169, 169, 169), (105, 105, 105)]  # Tonos de metal
]

# Crear una nueva matriz para representar los colores de los cuadrados
matriz_Blanca_Filo = [[(0, 0, 0) for _ in range(columnas)] for _ in range(filas)]
matriz_Blanca_Mango = [[(0, 0, 0) for _ in range(columnas)] for _ in range(filas)]

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
def generacion_procedural(matriz_Blanca_Filo, paletas, diferencia_minima):
    # Seleccionar una paleta aleatoria
    paleta = random.choice(paletas)
    
    # Generar un color base aleatorio
    color_base = random.choice(paleta)

    # Iterar sobre las filas y columnas de la matriz
    for i in range(filas):
        for j in range(columnas):
            # Seleccionar un color aleatorio de la paleta
            color_restringido = generar_color_con_restriccion(color_base, paletas, diferencia_minima)
            # Actualizar el color en la matriz
            matriz_Blanca_Filo[i][j] = color_restringido

# Generar la matriz de colores de forma procedural
generacion_procedural(matriz_Blanca_Filo, paletas_filos, 400)
generacion_procedural(matriz_Blanca_Mango, paletas_mangos, 200)

# Crear una nueva imagen en blanco
imagen_filo = Image.new("RGB", (ancho, altura), "black")
imagen_mango = Image.new("RGB", (ancho, altura), "black")

# Crear un objeto ImageDraw para dibujar en la imagen
DrawFilo = ImageDraw.Draw(imagen_filo)
DrawMango = ImageDraw.Draw(imagen_mango)

# Dibujar los cuadrados utilizando los colores de la matriz
for i in range(filas):
    for j in range(columnas):
        # Obtener el color de la matriz
        color_filo = matriz_Blanca_Filo[i][j]
        color_mango = matriz_Blanca_Mango[i][j]
        # Calcular las coordenadas del cuadrado
        #Para el filo:
        f_x0 = j * tamano_textura
        f_y0 = i * tamano_textura
        f_x1 = f_x0 + tamano_textura
        f_y1 = f_y0 + tamano_textura
        #Para el mango:
        m_x0 = j * tamano_textura
        m_y0 = i * tamano_textura
        m_x1 = m_x0 + tamano_textura
        m_y1 = m_y0 + tamano_textura
        # Dibujar el cuadrado
        DrawFilo.rectangle([(f_x0, f_y0), (f_x1, f_y1)], fill=color_filo)
        DrawMango.rectangle([(m_x0, m_y0), (m_x1, m_y1)], fill=color_mango)

# Guardar la imagen generada
imagen_filo.save("Textura.png")
imagen_mango.save("Textura_Mango.png")

# Cargar la imagen generada con cv2
imagen_filo = cv2.imread('Textura.png')
imagen_mango = cv2.imread('Textura_Mango.png')

#Definir los puntos en donde se podrá ensamblar el filo con el mango
punto_der_ensamble = random.randint(350, 450)
punto_izq_ensamble = random.randint(150, 250)

# Definir los puntos del mango
puntos_mango = np.array([[punto_izq_ensamble, 800],
                          [punto_izq_ensamble - random.randint(0,15), random.randint(795, 820)],
                          [punto_izq_ensamble - random.randint(0,15), random.randint(820, 880)],
                          [random.randint(250, 290), random.randint(820, 880)],
                          [random.randint(270, 295), random.randint(900, 1100)],
                          [random.randint(305, 325), random.randint(900, 1100)],
                          [random.randint(310, 350), random.randint(820, 880)],
                          [punto_der_ensamble + random.randint(0,15), random.randint(820, 880)],
                          [punto_der_ensamble + random.randint(0,15), 800],          
                          [punto_der_ensamble, 800]], np.int32)

# Definir los puntos de la espada
puntos_espada = np.array([[punto_der_ensamble, 800],
                          [random.randint(350, 450), random.randint(750, 780)],
                          [random.randint(350, 450), random.randint(550, 650)],
                          [random.randint(350, 450), random.randint(350, 450)],
                          [random.randint(350, 450), random.randint(150, 250)], 
                          [random.randint(150, 300), random.randint(50, 150)], 
                          [random.randint(150,250), random.randint(150,250)],
                          [random.randint(150,250), random.randint(450,550)],
                          [random.randint(150,250), random.randint(650,750)],         
                          [punto_izq_ensamble, 800]], np.int32)

# Crear una máscara en blanco con el mismo tamaño que la imagen
mascara_filo = np.zeros_like(imagen_filo)
mascara_mango = np.zeros_like(imagen_mango)

# Dibujar la forma de la espada en la máscara
cv2.fillPoly(mascara_filo, [puntos_espada], (255, 255, 255))
cv2.fillPoly(mascara_mango, [puntos_mango], (255, 255, 255))

# Aplicar la máscara a la imagen para recortarla
imagen_filo_recortada = cv2.bitwise_and(imagen_filo, mascara_filo)
imagen_mango_recortada = cv2.bitwise_and(imagen_mango, mascara_mango)

# Superponer imagen_filo_recortada sobre imagen_mango_recortada
Espada = cv2.addWeighted(imagen_filo_recortada, 1, imagen_mango_recortada, 1, 0)

# Definir las coordenadas de inicio y fin de la línea
x1, y1 = punto_der_ensamble, 800
x2, y2 = punto_izq_ensamble, 800

# Dibujar la línea negra en la imagen
grosor = 1
Espada = cv2.line(Espada, (x1, y1), (x2, y2), (0,0,0), grosor)

#Guardar la imagen en el archivo "Espada.png"
cv2.imwrite("Espada.png", Espada)

# Mostrar la imagen superpuesta
cv2.imshow('Espada', Espada)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Nivel del jugador (constante)
nivel = 13

# Empezamos con las estadísticas
# AF: Ataque físico
# AM: Ataque mágico
# VA: Velocidad de ataque
# RV: Robo de vida
# Dur: Durabilidad
# PC: Probabilidad de crítico
# DC: Daño crítico
def Estadisticas(nivel):
    AF=random.randint(nivel*1,nivel*5)
    AM=random.randint(nivel*1,nivel*5)
    VA=random.randint(nivel*1,nivel*5)
    RV=random.randint(nivel*1,nivel*5)
    Dur=random.randint(1,100)
    PC=random.randint(1,100)
    DC=random.randint(1,100)
    efecto=Efecto()
    arma=[AF,AM,VA,RV,Dur,PC,DC,efecto]
    
    return(arma)
def Efecto():
    efecto=random.choice(["Fuego","Hielo","Veneno","Luz","Oscuridad","Aturdimiento","Looteo"])
    return(efecto)
def Arma(nivel):
    arma=Estadisticas(nivel)
    
    prob=random.randint(1,100)
    if (prob<=10):
        efecto2=Efecto()
        arma=np.append(arma,efecto2)
    else:
        arma=np.append(arma,"   ")
    if (prob==1):
        efecto3=Efecto()
        arma=np.append(arma,efecto3)
    else:
        arma=np.append(arma,"   ")
    return arma

arma=Arma(nivel)
datos_arma=["Ataque fisico","Ataque magico","Velocidad de ataque","Robo de vida","Durabilidad","Probabilidad de critico","Dano critico","Efecto/s","    ","    "]
datos_finales=np.array([[datos_arma],[arma]])
datos_finales=datos_finales.T

with open("archivo.txt", "w") as archivo:
    for fila in datos_finales:
        fila_str = " ".join(map(str, fila))
        archivo.write(fila_str + "\n")
    archivo.close()
