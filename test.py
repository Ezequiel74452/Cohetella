import cv2
import numpy as np
import matplotlib.pyplot as plt

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
PISO = VID_HEIGHT - 477 # Calculado a ojo más o menos donde está la base del cohete (eje X)
ORIGEN = 268 # Calculado a ojo más o menos desde el centro del cohete (eje Y)
PX_TO_CM = 0.9047

# Rastreador CSRT
tracker = cv2.legacy.TrackerCSRT.create()

# Lee el primer fotograma
ret, frame = cap.read()
if not ret:
    print("No se pudo leer el video.")
    cap.release()
    cv2.destroyAllWindows()
    exit()

# Selección manual del área de la botella en el primer fotograma
# scale = 0.25
# small_frame = cv2.resize(frame, (int(VID_WIDTH * scale), int(VID_HEIGHT * scale)))
# bbox = cv2.selectROI(small_frame, False)
# bbox = [int(bbox[0] / scale), int(bbox[1] / scale), int(bbox[2] / scale), int(bbox[3] / scale)]

# (Lo comentado arriba es un intento de trackear el tiro vertical)
bbox = cv2.selectROI(frame, False)
tracker.init(frame, bbox)

# Listas para almacenar las coordenadas de la trayectoria
x_positions = []
y_positions = []

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Actualizar el rastreador
    success, bbox = tracker.update(frame)
    if success:
        x, y, w, h = [int(v) for v in bbox]
        center_x = x + w // 2
        center_y = y + h // 2
        # Guardar las posiciones de acuerdo a nuestro sistema de coordenadas
        x_positions.append(center_x-ORIGEN)
        y_positions.append(VID_HEIGHT-PISO-y + h // 2)
        print(f"X: {x_positions[-1]}, Y: {y_positions[-1]}")

        # Dibujar la caja y el centro
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

    # Mostrar el fotograma
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

# Graficar la trayectoria
X_POSITIONS_CM = np.array(x_positions)*PX_TO_CM
Y_POSITIONS_CM = np.array(y_positions)*PX_TO_CM
fig, axs = plt.subplots(1,2, figsize = (14,7))
plt.title('Trayectoria de la botella')
axs[0].plot(x_positions, y_positions, marker='o')
axs[0].set_xlabel('X (px)')
axs[0].set_ylabel('Y (px)')
axs[1].plot(X_POSITIONS_CM, Y_POSITIONS_CM, marker='o')
axs[1].set_xlabel('X (cm)')
axs[1].set_ylabel('Y (cm)')
plt.show()

# Gráfico viejo de la trayectoria en px
#plt.plot(x_positions, y_positions, marker='o')
#plt.xlabel('X (px)')
#plt.ylabel('Y (px)')
#plt.title('Trayectoria de la botella')
#plt.show()
