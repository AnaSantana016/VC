import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
import time

# Inicializar la cámara y el detector de manos
camera = cv2.VideoCapture(0)
hand_detector = HandDetector(maxHands=1)  # Definimos el número máximo de manos

# Configuración de parámetros
offset = 20  # Margen alrededor de la mano al recortar la imagen
imgSize = 300  # Tamaño deseado para la imagen recortada y redimensionada

folder = "C:/Direccion/Para/Guardar/Fotos/Dataset"
counter = 0

while True:
    # Capturar el fotograma actual de la cámara
    success, img = camera.read()

    # Detectar manos en la imagen
    hands, img = hand_detector.findHands(img)
    
    # Visualizar la imagen original
    cv2.imshow("Image", img)

    if hands:
        # Tomar la información de la primera mano detectadas
        hand = hands[0]
        x, y, w, h = hand['bbox']
        
        # Crear una imagen blanca del tamaño deseado
        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255

        # Recortar la región de la mano de la imagen original
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]
        
        # Obtener la forma de la región recortada
        imgCropShape = imgCrop.shape
        
        # Calcular la relación de aspecto de la mano
        aspectRatio = h / w
        
        if aspectRatio > 1:
            # Si la posición de la mano es más alta que ancha
            k = imgSize / h
            wCal = math.ceil(k * w)
            imgResize = cv2.resize(imgCrop, (wCal, imgSize))
            imgResizeShape = imgResize.shape
            wGap = int(math.ceil((imgSize - wCal) / 2))
            
            # Convertir a enteros y asignar la región redimensionada a la imagen blanca
            wGap = int(wGap)
            wCal = int(wCal)
            imgWhite[:, wGap:wCal + wGap] = imgResize
            
        else:
            # Si la mposición de la mano es más ancha que alta 
            k = imgSize / w
            hCal = math.ceil(k * h)
            imgResize = cv2.resize(imgCrop, (imgSize, hCal))
            imgResizeShape = imgResize.shape
            hGap = int(math.ceil((imgSize - hCal) / 2))
            
            # Convertir a enteros y asignar la región redimensionada a la imagen blanca
            imgWhite[hGap:hCal + hGap, :] = imgResize

        # Visualizar la imagen recortada y la imagen blanca
        cv2.imshow("ImageCrop", imgCrop)
        cv2.imshow("ImageWhite", imgWhite)
       
        
    key = cv2.waitKey(1)
    
    # Se espera a que se pulse la tecla "S" para sacar una captura de la posición de la mano
    if key == ord("s"):
        counter += 1
        cv2.imwrite(f'{folder}/Image_{time.time()}.jpg', imgWhite)
        print(counter)

    # Espera la tecla 'q' para cerrar la cámara
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar la ventana
camera.release()
cv2.destroyAllWindows()
