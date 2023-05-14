import cv2
import numpy as np

# Cargar el modelo de detección de objetos YOLOv8
net = cv2.dnn.readNetFromDarknet("yolov8n")

# Definir las clases de objetos que queremos detectar
classes = ["clase1", "clase2", "clase3"]

# Cargar la imagen y redimensionarla para la entrada del modelo
img = cv2.imread("imagen.jpg")
height, width, channels = img.shape
blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)

# Establecer las entradas y salidas del modelo
net.setInput(blob)
output_layers = net.getUnconnectedOutLayersNames()
layer_outputs = net.forward(output_layers)

# Inicializar las listas de coordenadas y distancias de los objetos detectados
boxes = []
confidences = []
class_ids = []
distances = []

# Recorrer las salidas del modelo para obtener las coordenadas de los objetos detectados
for output in layer_outputs:
    for detection in output:
        scores = detection[5:]
        class_id = np.argmax(scores)
        confidence = scores[class_id]
        if confidence > 0.5 and classes[class_id] in classes:
            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)
            w = int(detection[2] * width)
            h = int(detection[3] * height)
            x = center_x - w // 2
            y = center_y - h // 2
            boxes.append([x, y, w, h])
            confidences.append(float(confidence))
            class_ids.append(class_id)

# Aplicar la supresión no máxima para eliminar detecciones redundantes
indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

# Calcular la distancia de los objetos detectados
for i in range(len(boxes)):
    if i in indexes:
        x, y, w, h = boxes[i]
        # Calcular la distancia en función del tamaño del objeto en la imagen
        # y de la distancia focal de la cámara
        distance = (objeto_tamano_real * distancia_focal) / w
        distances.append(distance)

# Imprimir las distancias de los objetos detectados
for distance in distances:
    print("Distancia del objeto: ", distance)