import cv2
import numpy as np
import matplotlib.pyplot as plt
import utilsVideo as uv


### IMPORTANTE (USO)
### Cuando se abre el primer frame, hay que seleccionar un área (el cohete) a trackear.
### Clickear en una esquina cercana al cohete y mantener para formar el cuadrado.
### Luego, enter para confirmar la selección y el trackeo empieza automáticamente.

# Cargar video
cap = cv2.VideoCapture('naranja.mp4') # Tiro oblicuo mio (poner el video en el mismo directorio y
#																					con el mismo nombre o cambiar la ambas cosas)

# Constantes útiles
VID_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
VID_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(VID_WIDTH, VID_HEIGHT)
PISO = 942 # Calculado a ojo más o menos donde está la base del cohete (eje X)
ORIGEN = 268 # Calculado a ojo más o menos desde el centro del cohete (eje Y)
PX_TO_CM = 0.64286
FPS = 240

# Rastreador CSRT
tracker = cv2.legacy.TrackerCSRT.create()

# Lee el primer fotograma
ret, frame = cap.read()
if not ret:
    print("No se pudo leer el video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()


frame_resized = uv.rescaleFrame(frame, scale=.5)

# (Lo comentado arriba es un intento de trackear el tiro vertical)
bbox = cv2.selectROI(frame_resized, False)
tracker.init(frame_resized, bbox)

# Listas para almacenar las coordenadas de la trayectoria
y_positions = []
times = []

frame_number = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_resized = uv.rescaleFrame(frame, scale=.5)
    # Actualizar el rastreador
    success, bbox = tracker.update(frame_resized)
    if success:
        x, y, w, h = [int(v) for v in bbox]
        center_x = x + w // 2
        center_y = y + h // 2

        final_y = VID_HEIGHT - PISO - (center_y * 2)

        # Guardar las posiciones de acuerdo a nuestro sistema de coordenadas
        y_positions.append(final_y)

        # Calcular el tiempo correspondiente a este fotograma
        time_elapsed = frame_number / FPS  # Tiempo en segundos
        times.append(time_elapsed)

        print(f"Y: {y_positions[-1]} en t = {time_elapsed:.2f} s")

        # Dibujar la caja y el centro
        cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame_resized, (center_x, center_y), 5, (0, 0, 255), -1)

    frame_number += 1

    # Mostrar el fotograma
    cv2.imshow('Tracking', frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Graficar la posición
y_positions_m = np.array(y_positions) * PX_TO_CM * 100
plt.title('Posición de la botella en el tiempo')
plt.plot(times, y_positions_m, marker='o')
plt.xlabel('Tiempo (s)')
plt.ylabel('Y (cm)')
plt.grid(True)
plt.show()

# Gráfico viejo de la trayectoria en px
#plt.plot(x_positions, y_positions, marker='o')
#plt.xlabel('X (px)')
#plt.ylabel('Y (px)')
#plt.title('Trayectoria de la botella')
#plt.show()
