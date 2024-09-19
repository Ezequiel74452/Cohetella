import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import utilsVideo as uv

"""

### IMPORTANTE (USO)
### Cuando se abre el primer frame, hay que seleccionar un área (el cohete) a trackear.
### Clickear en una esquina cercana al cohete y mantener para formar el cuadrado.
### Luego, enter para confirmar la selección y el trackeo empieza automáticamente.
# Cargar video
cap = cv2.VideoCapture('videos/rojo.MOV') # Tiro oblicuo mio (poner el video en el mismo directorio y
#																					con el mismo nombre o cambiar la ambas cosas)

# Constantes útiles
VID_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
VID_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
PISO = VID_HEIGHT - 477 # Calculado a ojo más o menos donde está la base del cohete (eje X)
ORIGEN = 268 # Calculado a ojo más o menos desde el centro del cohete (eje Y)
FPS = 240

datos = {'Tiempo (s)':np.array([]), 'Posición Y (px)':np.array([]), 'Posición X (px)':np.array([])}
df = pd.DataFrame(data=datos)

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

frame_number = 0

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
		final_x = center_x-ORIGEN
		final_y = VID_HEIGHT-PISO-y + h // 2
		time_elapsed = frame_number / FPS
    
		datos_frame = {'Tiempo (s)':[time_elapsed], 'Posición Y (px)':[final_y], 'Posición X (px)':[final_x]}
		df_frame = pd.DataFrame(data=datos_frame)
		df = pd.concat([df, df_frame], ignore_index=True)

		# Dibujar la caja y el centro
		cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

	frame_number += 1

	# Mostrar el fotograma
	cv2.imshow('Tracking', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()

#Calcular posición en metros
df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: uv.fromPixelsToMetersOblicuo(x))
df['Posición X (m)'] = df['Posición X (px)'].apply(lambda x: uv.fromPixelsToMetersOblicuo(x))

def smooth_positions(positions, window_size=10):
    return np.convolve(positions, np.ones(window_size)/window_size, mode='valid')

# Aumentar el tamaño de la ventana (window_size) para suavizar más
smoothed_positions_y = smooth_positions(df['Posición Y (m)'], window_size=10)
smoothed_positions_x = smooth_positions(df['Posición X (m)'], window_size=10)
df = df.iloc[:len(smoothed_positions_y)]

# Calcular las velocidades 
df['Velocidad Y (m/s)'] = df['Posición Y (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
df['Velocidad Y (m/s)'] = df['Velocidad Y (m/s)'].fillna(0)
df['Velocidad X (m/s)'] = df['Posición X (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
df['Velocidad X (m/s)'] = df['Velocidad X (m/s)'].fillna(0)

#Calcular la aceleración 
df['Aceleración Y (m/s^2)'] = df['Velocidad Y (m/s)'].diff(periods=5) / df['Tiempo (s)'].diff(periods=5)
df['Aceleración Y (m/s^2)'] = df['Aceleración Y (m/s^2)'].fillna(0)
df['Aceleración X (m/s^2)'] = df['Velocidad X (m/s)'].diff(periods=5) / df['Tiempo (s)'].diff(periods=5)
df['Aceleración X (m/s^2)'] = df['Aceleración X (m/s^2)'].fillna(0)

print(df)
df.to_csv('data_oblicuo.csv', index=False)

# Graficar la posición en Y suavizada
#plt.title('Posición de la botella en el eje Y con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Posición Y (m)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Posición (m)')
#plt.grid(True)
#plt.show()

# Graficar la posición en X suavizada
#plt.title('Posición de la botella en el eje X con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Posición X (m)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Posición (m)')
#plt.grid(True)
#plt.show()

"""

df = pd.read_csv('data_oblicuo.csv')

# Graficar las posiciones suavizadas
fig, axs = plt.subplots(1,3, figsize = (14,7))
plt.title('Trayectoria de la botella')
axs[0].plot(df['Tiempo (s)'], df['Posición X (m)'], marker='o')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('X (m)')
axs[1].plot(df['Tiempo (s)'], df['Posición Y (m)'], marker='o')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Y (m)')
axs[2].plot(df['Posición X (m)'], df['Posición Y (m)'], marker='o')
axs[2].set_xlabel('X (m)')
axs[2].set_ylabel('Y (m)')
plt.show()

# Graficar la velocidad con posiciones suavizadas
fig, axs = plt.subplots(1,2, figsize = (14,7))
plt.title('Velocidad de la botella')
axs[0].plot(df['Tiempo (s)'], df['Velocidad X (m/s)'], marker='o')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('Vel_X (m/s)')
axs[1].plot(df['Tiempo (s)'], df['Velocidad Y (m/s)'], marker='o')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('Vel_Y (m/s)')
plt.show()

# Graficar la aceleración con posiciones suavizadas
fig, axs = plt.subplots(1,2, figsize = (14,7))
plt.title('Aceleración de la botella')
axs[0].plot(df['Tiempo (s)'], df['Aceleración X (m/s^2)'], marker='o')
axs[0].set_xlabel('Tiempo (s)')
axs[0].set_ylabel('A_X (m/s^2)')
axs[1].plot(df['Tiempo (s)'], df['Aceleración Y (m/s^2)'], marker='o')
axs[1].set_xlabel('Tiempo (s)')
axs[1].set_ylabel('A_Y (m/s^2)')
plt.show()


# Graficar la velocidad con posiciones suavizadas
#plt.title('Velocidad de la botella en el eje Y con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Velocidad Y (m/s)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Velocidad (m/s)')
#plt.grid(True)
#plt.show()

# Graficar la velocidad con posiciones suavizadas
#plt.title('Velocidad de la botella en el eje X con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Velocidad X (m/s)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Velocidad (m/s)')
#plt.grid(True)
#plt.show()

# Graficar la aceleración con posiciones suavizadas
#plt.title('Aceleración de la botella en el eje Y con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Aceleración Y (m/s^2)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Aceleración (m/s^2)')
#plt.grid(True)
#plt.show()

# Graficar la aceleración con posiciones suavizadas
#plt.title('Aceleración de la botella en el eje X con respecto al tiempo')
#plt.plot(df['Tiempo (s)'], df['Aceleración X (m/s^2)'], marker='o')
#plt.xlabel('Tiempo (s)')
#plt.ylabel('Aceleración (m/s^2)')
#plt.grid(True)
#plt.show()

# Graficar la trayectoria
#X_POSITIONS_CM = np.array(x_positions)*PX_TO_CM
#Y_POSITIONS_CM = np.array(y_positions)*PX_TO_CM
#fig, axs = plt.subplots(1,2, figsize = (14,7))
#plt.title('Trayectoria de la botella')
#axs[0].plot(x_positions, y_positions, marker='o')
#axs[0].set_xlabel('X (px)')
#axs[0].set_ylabel('Y (px)')
#axs[1].plot(X_POSITIONS_CM, Y_POSITIONS_CM, marker='o')
#axs[1].set_xlabel('X (cm)')
#axs[1].set_ylabel('Y (cm)')
#plt.show()

# Gráfico viejo de la trayectoria en px
#plt.plot(x_positions, y_positions, marker='o')
#plt.xlabel('X (px)')
#plt.ylabel('Y (px)')
#plt.title('Trayectoria de la botella')
#plt.show()
