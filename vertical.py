import cv2
import numpy as np
import matplotlib.pyplot as plt
import utilsVideo as uv
import pandas as pd
from sympy import *
from scipy.optimize import curve_fit

### IMPORTANTE (USO)
### Cuando se abre el primer frame, hay que seleccionar un área (el cohete) a trackear.
### Clickear en una esquina cercana al cohete y mantener para formar el cuadrado.
### Luego, enter para confirmar la selección y el trackeo empieza automáticamente.


# Cargar video
cap = cv2.VideoCapture('videos/120fps.mp4') 

# Constantes útiles
VID_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
VID_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
PISO = 942 # Calculado a ojo más o menos donde está la base del cohete (eje X)
ORIGEN = 268 # Calculado a ojo más o menos desde el centro del cohete (eje Y)
FPS = 120

datos = {'Tiempo (s)':np.array([]),
        'Posición Y (px)':np.array([])}

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


frame_resized = uv.rescaleFrame(frame, scale=.5)

bbox = cv2.selectROI(frame_resized, False)
tracker.init(frame_resized, bbox)

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

        # Guardar las posiciones de acuerdo a nuestro sistema de coordenadas
        final_y = VID_HEIGHT - PISO - (center_y * 2)

        # Calcular el tiempo correspondiente a este fotograma
        time_elapsed = frame_number / FPS  # Tiempo en segundos

        datos_frame = {'Tiempo (s)':[time_elapsed],
             'Posición Y (px)':[final_y]}

        df_frame = pd.DataFrame(data=datos_frame)
        df = pd.concat([df, df_frame], ignore_index=True)

        print(f"Y: {final_y}, Tiempo: {time_elapsed}")

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

#Calcular posición en metros
df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: uv.fromPixelsToMeters(x))

def smooth_positions(positions, window_size=10):
    return np.convolve(positions, np.ones(window_size)/window_size, mode='valid')

# Aumentar el tamaño de la ventana (window_size) para suavizar más
smoothed_positions = smooth_positions(df['Posición Y (m)'], window_size=10)
df = df.iloc[:len(smoothed_positions)]
#df['Posición Y (m)'] = smoothed_positions

# Calcular las velocidades 
df['Velocidad (m/s)'] = df['Posición Y (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
df['Velocidad (m/s)'] = df['Velocidad (m/s)'].fillna(0)

#Calcular la aceleración 
df['Aceleración (m/s^2)'] = df['Velocidad (m/s)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
df['Aceleración (m/s^2)'] = df['Aceleración (m/s^2)'].fillna(0)

print(df)
df.to_csv('data.csv', index=False)

"""
# Graficar la posición suavizada
plt.title('Posición de la botella en el tiempo')
plt.plot(df['Tiempo (s)'], df['Posición Y (m)'], marker='o')
plt.xlabel('Tiempo (s)')
plt.ylabel('Posición (m)')
plt.grid(True)
plt.show()

# Graficar la velocidad con posiciones suavizadas
plt.title('Velocidad de la botella en el tiempo')
plt.plot(df['Tiempo (s)'], df['Velocidad (m/s)'], marker='o')
plt.xlabel('Tiempo (s)')
plt.ylabel('Velocidad (m/s)')
plt.grid(True)
plt.show()

# Graficar la aceleración con posiciones suavizadas
plt.title('Aceleración de la botella en el tiempo')
plt.plot(df['Tiempo (s)'], df['Aceleración (m/s^2)'], marker='o')
plt.xlabel('Tiempo (s)')
plt.ylabel('Aceleración (m/s^2)')
plt.grid(True)
plt.show()
"""


#Creamos una figura con 3 filas y 1 columna
fig, axs=plt.subplots(3, 1,figsize=(10, 10))

#Graficamos la posición
axs[0].plot(df['Tiempo (s)'], df['Posición Y (m)'])
axs[0].set_title('Posición de la botella en el tiempo')
axs[0].set_ylabel('Posición (m)')
axs[0].grid(True)

#Graficamos la velocidad
axs[1].plot(df['Tiempo (s)'], df['Velocidad (m/s)'], color='green', marker='.')
axs[1].set_title('Velocidad de la botella en el tiempo')
axs[1].set_ylabel('Velocidad (m/s)')
axs[1].grid(True)

#Graficamos la aceleración
axs[2].plot(df['Tiempo (s)'], df['Aceleración (m/s^2)'], color='orange', marker='.')
axs[2].set_title('Aceleración de la botella en el tiempo')
axs[2].set_ylabel('Aceleración (m/s^2)')
axs[2].set_xlabel('Tiempo (s)')
axs[2].grid(True)

plt.tight_layout()
plt.show()

""""
#Condiciones iniciales de velocidad y posición
v0 = 0
y0 = 0

def velocity(t,g,vo):
  return(g*t+vo)

popt, pcov = curve_fit(velocity, xdata = df['Tiempo (s)'], ydata = df['Velocidad (m/s)'], p0 = [9.8, 0])
errs = np.sqrt(np.diag(pcov))
print(popt,errs)

"""