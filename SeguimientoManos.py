
#------------------------------Importamos las librerias -----------------------------------
import math
import cv2
import mediapipe as mp
import time

#-------------------------------- Creamos una clase---------------------------------
class detectormanos():
    #-------------------Inicializamos los parametros de la deteccion----------------
    def __init__(self, mode=False, maxManos = 2, model_complexity=1, Confdeteccion = 0.5, Confsegui = 0.5):
        self.mode = mode          #Creamos el objeto y el tendra su propia variable
        self.maxManos = maxManos  #Lo mismo haremos con todos los objetos
        self.compl = model_complexity
        self.Confdeteccion = Confdeteccion
        self.Confsegui = Confsegui

        # ---------------------------- Creamos los objetos que detectaran las manos y las dibujaran----------------------
        self.mpmanos = mp.solutions.hands
        # Configuración básica sin visualización
        self.manos = self.mpmanos.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxManos,
            model_complexity=self.compl,
            min_detection_confidence=self.Confdeteccion,
            min_tracking_confidence=self.Confsegui
        )
        self.tip = [4,8,12,16,20]

    #----------------------------------------Funcion para encontrar las manos-----------------------------------
    def encontrarmanos(self, frame, dibujar = False):
        imgcolor = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.resultados = self.manos.process(imgcolor)
        # No dibujamos nada, solo procesamos
        return frame

    #------------------------------------Funcion para encontrar la posicion----------------------------------
    def encontrarposicion(self, frame, ManoNum = 0, dibujar = False):
        xlista = []
        ylista = []
        bbox = []
        player = 0
        self.lista = []
        if self.resultados.multi_hand_landmarks:
            miMano = self.resultados.multi_hand_landmarks[ManoNum]
            prueba = self.resultados.multi_hand_landmarks
            player = len(prueba)
            #print(player)
            for id, lm in enumerate(miMano.landmark):
                alto, ancho, c = frame.shape  # Extraemos las dimensiones de los fps
                cx, cy = int(lm.x * ancho), int(lm.y * alto)  # Convertimos la informacion en pixeles
                xlista.append(cx)
                ylista.append(cy)
                self.lista.append([id, cx, cy])
                # Quitamos el dibujo de los círculos

            xmin, xmax = min(xlista), max(xlista)
            ymin, ymax = min(ylista), max(ylista)
            bbox = xmin, ymin, xmax, ymax
            # Quitamos el dibujo del rectángulo
        return self.lista, bbox, player

    #----------------------------------Funcion para detectar y dibujar los dedos arriba------------------------
    def dedosarriba(self):
        dedos = []
        if self.lista[self.tip[0]][1] > self.lista[self.tip[0]-1][1]:
            dedos.append(1)
        else:
            dedos.append(0)

        for id in range (1,5):
            if self.lista[self.tip[id]][2] < self.lista[self.tip[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)

        return dedos

    #--------------------------- Funcion para detectar la distancia entre dedos----------------------------
    def distancia(self, p1, p2, frame, dibujar = False):
        x1, y1 = self.lista[p1][1:]
        x2, y2 = self.lista[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
        # Quitamos el dibujo de las líneas y círculos
        length = math.hypot(x2-x1, y2-y1)

        return length, frame, [x1, y1, x2, y2, cx, cy]

#----------------------------------------------- Funcion principal-------------------- ----------------------------
def main():
    ptiempo = 0
    ctiempo = 0

    # -------------------------------------Leemos la camara web ---------------------------------------------
    cap = cv2.VideoCapture(0)
    #-------------------------------------Crearemos el objeto -------------------------------------
    detector = detectormanos()
    # ----------------------------- Realizamos la deteccion de manos---------------------------------------
    while True:
        ret, frame = cap.read()
        #Una vez que obtengamos la imagen la enviaremos
        frame = detector.encontrarmanos(frame)
        lista, bbox = detector.encontrarposicion(frame)
        #if len(lista) != 0:
            #print(lista[4])
        # ----------------------------------------Mostramos los fps ---------------------------------------
        ctiempo = time.time()
        fps = 1 / (ctiempo - ptiempo)
        ptiempo = ctiempo

        cv2.putText(frame, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

        cv2.imshow("Manos", frame)
        k = cv2.waitKey(1)

        if k == 27:
            break
    cap.release()
    cv2.destroyAllWindows()




if __name__ == "__main__":
    main()
