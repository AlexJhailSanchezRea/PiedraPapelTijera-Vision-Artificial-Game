# Importamos las librerias
import cv2
import random
import SeguimientoManos as sm  # Clase manos
import os
import imutils
import numpy as np
import time
import math

# Declaracion de variables
fs = False
fu = False      # Bandera up
fd = False      # Bandera down
fj = False      # Bandera juego
fr = False      # Bandera reset
fgia = False    # Bandera gana IA
fgus = False    # Bandera gana Usuario
femp = False    # Bandera empate
fder = False    # Bandera derecha
fizq = False    # Bandera izquierda
conteo = 0

# Accedemos a la carpeta
path = 'Imagenes'
images = []
clases = []
lista = os.listdir(path)

# Leemos los rostros del DB
for lis in lista:
    # Leemos las imagenes de los rostros
    imgdb = cv2.imread(f'{path}/{lis}')
    # Almacenamos imagen
    images.append(imgdb)
    # Almacenamos nombre
    clases.append(os.path.splitext(lis)[0])

print(clases)

# Lectura de la camara
cap = cv2.VideoCapture(0)

# Declaramos el detector
detector = sm.detectormanos(Confdeteccion=0.9)

# Añadir variables para marcador y rondas
rondas = 0
puntos_ia = 0
puntos_usuario = 0

# Después de la sección de lectura de imágenes, añadir función de procesamiento de imágenes
def process_game_image(image, target_size=(240, 240)):
    try:
        if image is None:
            return None
        # Redimensionar la imagen manteniendo la proporción
        h, w = image.shape[:2]
        aspect = w/h
        if aspect > 1:
            new_w = target_size[0]
            new_h = int(new_w/aspect)
        else:
            new_h = target_size[1]
            new_w = int(new_h*aspect)
        
        resized = cv2.resize(image, (new_w, new_h))
        
        # Crear un lienzo del tamaño objetivo
        canvas = np.zeros((target_size[1], target_size[0], 3), dtype=np.uint8)
        
        # Calcular posición para centrar la imagen
        y_offset = (target_size[1] - new_h) // 2
        x_offset = (target_size[0] - new_w) // 2
        
        # Colocar la imagen redimensionada en el centro
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        return canvas
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

# Procesar todas las imágenes al cargarlas
processed_images = []
for img in images:
    processed = process_game_image(img)
    if processed is not None:
        processed_images.append(processed)
    else:
        print(f"Error: No se pudo procesar una imagen")
        # Crear una imagen de respaldo con texto
        backup = np.zeros((240, 240, 3), dtype=np.uint8)
        cv2.putText(backup, "Error", (70, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
        processed_images.append(backup)

# Reemplazar la lista original de imágenes
images = processed_images

# Definir colores constantes
VERDE_OSCURO = (0, 100, 0)  # Verde oscuro
NEGRO = (0, 0, 0)          # Negro
GRIS_OSCURO = (50, 50, 50) # Gris oscuro para algunos detalles

def draw_super_futuristic_hud(frame):
    height, width = frame.shape[:2]
    
    # Marco exterior con efecto metálico
    cv2.rectangle(frame, (10, 10), (width-10, height-10), VERDE_OSCURO, 3)
    cv2.rectangle(frame, (20, 20), (width-20, height-20), NEGRO, 2)
    
    # Esquinas reforzadas
    corner_points = [(20,20), (width-20,20), (20,height-20), (width-20,height-20)]
    for corner in corner_points:
        # Efecto de tornillos metálicos
        cv2.circle(frame, corner, 15, VERDE_OSCURO, -1)
        cv2.circle(frame, corner, 10, NEGRO, 2)
        cv2.circle(frame, corner, 5, GRIS_OSCURO, -1)
    
    return frame

def draw_text_with_glow(frame, text, position, font_scale=1.0, thickness=2):
    # Sombra gris oscura
    cv2.putText(frame, text, (position[0]+2, position[1]+2), 
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, GRIS_OSCURO, thickness+1)
    # Texto principal en verde oscuro
    cv2.putText(frame, text, position, 
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, VERDE_OSCURO, thickness)

def draw_result_screen(frame, result_image, text):
    try:
        height, width = frame.shape[:2]
        
        # Mostrar imagen de resultado
        if result_image is None or result_image.size == 0:
            result_image = np.zeros((240, 240, 3), dtype=np.uint8)
            cv2.putText(result_image, text, (30, 120), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, VERDE_OSCURO, 2)
        
        alig, anig = result_image.shape[:2]
        y_pos = 70
        x_pos = 180
        
        # Marco del resultado
        cv2.rectangle(frame, (x_pos-15, y_pos-15), 
                     (x_pos+anig+15, y_pos+alig+15), 
                     VERDE_OSCURO, 3)
        cv2.rectangle(frame, (x_pos-10, y_pos-10), 
                     (x_pos+anig+10, y_pos+alig+10), 
                     NEGRO, 2)
        
        # Mostrar imagen
        frame[y_pos:y_pos+alig, x_pos:x_pos+anig] = result_image
        
        # Textos
        draw_text_with_glow(frame, text, (x_pos, y_pos+alig+40), 1.2)
        draw_text_with_glow(frame, "PRESIONA R PARA REVANCHA", 
                          (x_pos, y_pos+alig+80), 0.8)
        
        return frame
    except Exception as e:
        print(f"Error en draw_result_screen: {e}")
        return frame

# Función para guardar capturas de pantalla
def save_screenshot(frame, name):
    if not os.path.exists('screenshots'):
        os.makedirs('screenshots')
    cv2.imwrite(f'screenshots/{name}.png', frame)

# Empezamos
while True:
    # Lectura de la videocaptura
    ret, frame = cap.read()

    # Aplicar efectos futuristas
    frame = draw_super_futuristic_hud(frame)

    # Leemos teclado
    t = cv2.waitKey(1)

    # Extraemos la mitad del frame
    al, an, c = frame.shape
    cx = int(an/2)
    cy = int(al/2)

    # Espejo
    frame = cv2.flip(frame,1)

    # Encontramos las manos sin dibujar
    frame = detector.encontrarmanos(frame, dibujar=False)
    # Posiciones mano 1 sin dibujar
    lista1, bbox1, jug = detector.encontrarposicion(frame, ManoNum=0, dibujar=False)

    # 1 Jugador
    if jug == 1:
        # Dividimos pantalla con línea neón
        # cv2.line(frame, (cx,0), (cx,480), (0,255,255), 2)
        
        # Fondo semitransparente para textos
        overlay = frame.copy()
        cv2.rectangle(overlay, (245, 25), (380, 60), NEGRO, -1)
        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        draw_text_with_glow(frame, '1 JUGADOR', (250, 50), 1.0)
        overlay = frame.copy()
        cv2.rectangle(overlay, (145, 425), (465, 460), NEGRO, -1)
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        draw_text_with_glow(frame, 'PRESIONA S PARA EMPEZAR', (150, 450), 0.71)

        # Presiona S
        if t == 83 or t == 115 or fs == True:
            # Cambiamos bandera 's'
            fs = True
            # Obtenemos posicion de la mano
            if len(lista1) != 0:
                # Extraemos las coordenadas del dedo corazon
                x1, y1 = lista1[9][1:]

                #print(conteo)
                # Conteo de juego
                if conteo <= 2:
                    # Leemos la imagen inicial
                    #print(name)
                    img = images[conteo]
                    # Redimensionamos
                    img = imutils.resize(img, width=240, height=240)
                    ali, ani, c = img.shape

                    # Definimos en que parte de la pantalla esta
                    # Izquierda
                    if x1 < cx:
                        # Banderas Lado
                        fizq = True
                        fder = False
                        # Mostramos imagen
                        frame[130: 130 + ali, 350: 350 + ani] = img

                        # Empezamos conteo
                        # Superamos el Umbral
                        if y1 < cy - 40 and fd == False:
                            fu = True
                            cv2.circle(frame, (cx, cy), 5, (255, 255, 0), -1)
                            # cv2.line(frame, (cx - cx, cy-40), (an, cy-40), (0, 0, 0), 1)

                        # Bajamos del Umbral con Flag
                        elif y1 > cy - 40 and fu == True:
                            conteo = conteo + 1
                            fu = False

                    # Derecha
                    elif x1 > cx:
                        # Banderas Lado
                        fder = True
                        fizq = False
                        # Mostramos la imagen
                        frame[130: 130 + ali, 30: 30 + ani] = img

                        # Empezamos conteo
                        # Superamos el Umbral
                        if y1 < cy - 40 and fd == False:
                            fu = True
                            cv2.circle(frame, (cx,cy), 5, (255,255,0), -1)
                            #cv2.line(frame, (cx - cx, cy-40), (an, cy-40), (0, 0, 0), 1)

                        # Bajamos del Umbral con Flag
                        elif y1 > cy - 40 and fu == True:
                            conteo = conteo + 1
                            fu = False
                # Jugamos
                elif conteo == 3:
                    # Si no hemos jugado jugamos
                    if fj == False and fr == False:
                        # Elegimos piedra papel o tijera
                        juego = random.randint(3,5)
                        fj = True

                    # Izquierda
                    if fizq == True and fder == False:
                        # Mostramos
                        img = images[juego]
                        # Redimensionamos
                        img = imutils.resize(img, width=240, height=240)
                        ali, ani, c = img.shape
                        # Mostramos imagen
                        frame[130: 130 + ali, 350: 350 + ani] = img
                        print(juego)

                        # Si ya jugamos
                        if fj == True and fr == False:
                            # Extraemos valores de interes
                            # Punta DI
                            x2, y2 = lista1[8][1:]
                            # Punta DC
                            x3, y3 = lista1[12][1:]
                            # Punta DA
                            x4, y4 = lista1[16][1:]

                            # Falange DI
                            x22, y22 = lista1[6][1:]
                            # Falange DC
                            x33, y33 = lista1[10][1:]
                            # Falange DA
                            x44, y44 = lista1[14][1:]

                            # Condiciones de posicion
                            # Piedra
                            if x2 < x22 and x3 < x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # EMPATE
                                    print('EMPATE')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                                elif juego == 5:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True


                            # Papel
                            elif x2 > x22 and x3 > x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    fr = True
                                    femp = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True

                            # Tijera
                            elif x2 > x22 and x3 > x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA EL USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                        # Mostramos ganador
                        # IA
                        if fgia == True:
                            gan = images[6]
                            frame = draw_result_screen(frame, gan, "LA IA DOMINA")
                            
                        # USUARIO
                        elif fgus == True:
                            gan = images[7]
                            frame = draw_result_screen(frame, gan, "VICTORIA HUMANA")
                            
                        # EMPATE
                        elif femp == True:
                            gan = images[8]
                            frame = draw_result_screen(frame, gan, "EMPATE TÉCNICO")

                    # Derecha
                    if fizq == False and fder == True:
                        # Mostramos
                        img = images[juego]
                        # Redimensionamos
                        img = imutils.resize(img, width=240, height=240)
                        ali, ani, c = img.shape
                        # Mostramos imagen
                        frame[130: 130 + ali, 30: 30 + ani] = img
                        print(juego)

                        # Si ya jugamos
                        if fj == True and fr == False:
                            # Extraemos valores de interes
                            # Punta DI
                            x2, y2 = lista1[8][1:]
                            # Punta DC
                            x3, y3 = lista1[12][1:]
                            # Punta DA
                            x4, y4 = lista1[16][1:]

                            # Falange DI
                            x22, y22 = lista1[6][1:]
                            # Falange DC
                            x33, y33 = lista1[10][1:]
                            # Falange DA
                            x44, y44 = lista1[14][1:]

                            # Condiciones de posicion
                            # Piedra
                            if x2 > x22 and x3 > x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # EMPATE
                                    print('EMPATE')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                                elif juego == 5:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True


                            # Papel
                            elif x2 < x22 and x3 < x33 and x4 < x44:
                                # IA PAPEL
                                if juego == 3:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    fr = True
                                    femp = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True

                            # Tijera
                            elif x2 < x22 and x3 < x33 and x4 > x44:
                                # IA PAPEL
                                if juego == 3:
                                    # GANA EL USUARIO
                                    print('GANA EL HUMANO')
                                    # Bandera Ganador
                                    fgia = False
                                    fgus = True
                                    femp = False
                                    fr = True
                                # IA PIEDRA
                                elif juego == 4:
                                    # GANA LA IA
                                    print('GANA LA IA')
                                    # Bandera Ganador
                                    fgia = True
                                    fgus = False
                                    femp = False
                                    fr = True
                                elif juego == 5:
                                    # EMPATE
                                    print('EMPATE')
                                    fgia = False
                                    fgus = False
                                    femp = True
                                    fr = True

                        # Mostramos ganador
                        # IA
                        if fgia == True:
                            gan = images[6]
                            frame = draw_result_screen(frame, gan, "LA IA DOMINA")
                            
                        # USUARIO
                        elif fgus == True:
                            gan = images[7]
                            frame = draw_result_screen(frame, gan, "VICTORIA HUMANA")
                            
                        # EMPATE
                        elif femp == True:
                            gan = images[8]
                            frame = draw_result_screen(frame, gan, "EMPATE TÉCNICO")

    # 2 Jugadores
    elif jug == 2:
        # Encontramos la segunda mano sin dibujar
        lista2, bbox2, jug2 = detector.encontrarposicion(frame, ManoNum=1, dibujar=False)

        # Quitamos las líneas divisorias
        # cv2.line(frame, (cx, 0), (cx, 240), (255, 0, 0), 2)
        # cv2.line(frame, (cx, 240), (cx, 480), (0, 255, 0), 2)

        # Mostramos jugadores
        cv2.rectangle(frame, (245, 25), (408, 60), NEGRO, -1)
        draw_text_with_glow(frame, '2 JUGADORES', (250, 50), 0.71)

    # 0 Jugadores
    elif jug == 0:
        # Mostramos jugadores
        cv2.rectangle(frame, (225, 25), (388, 60), NEGRO, -1)
        draw_text_with_glow(frame, '0 JUGADORES', (230, 50), 0.71)

    # Logo o texto personalizado
    draw_text_with_glow(frame, 'BATALLA DE PIEDRA PAPEL TIJERA', (an//2-300, 35), 1.2)

    # Mostramos frames en tamaño tipo Epic Games y permitimos maximizar/restaurar
    frame = cv2.resize(frame, (1100, 600))  # Tamaño tipo Epic Games
    cv2.namedWindow("JUEGO CON AI", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("JUEGO CON AI", 1800, 1000)
    cv2.imshow("JUEGO CON AI", frame)
    if t == 27:
        break
    # Reset
    if t == 82 or t == 114:
        fs = False
        fu = False
        fd = False
        fj = False
        fr = False
        fgia = False
        fgus = False
        femp = False
        fder = False
        fizq = False
        conteo = 0
cap.release()
cv2.destroyAllWindows()
