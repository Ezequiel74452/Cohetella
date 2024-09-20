import cv2
import numpy as np
import matplotlib.pyplot as plt
from utilsGraficas import *
import utilsVideo as uv
import pandas as pd
from sympy import *
from scipy.optimize import curve_fit

### IMPORTANTE (USO)
### Cuando se abre el primer frame, hay que seleccionar un área (el cohete) a trackear.
### Clickear en una esquina cercana al cohete y mantener para formar el cuadrado.
### Luego, enter para confirmar la selección y el trackeo empieza automáticamente.
### Al finalizar se generara un csv con los datos capturados, y se podra elegir si generar la grafica en el momento.

#colores de las graficas:
C_POS = 'black'
C_VEL = 'blue'
C_ACC = 'red'

#graficar csv o trackear video
graficar = input("Graficar data.csv o trackear video?(1/2): ")
if(graficar == "1"):
    graficar_csv_plotly(C_POS,C_VEL,C_ACC)
    #graficar_csv_matplot()
    exit()

# Cargar video
videoCapturado = cv2.VideoCapture('videos/120fps.mp4') 

# Revisa que el video sea válido
ret, primerFrame = videoCapturado.read()
if not ret:
    print("No se pudo leer el video.")
    videoCapturado.release()
    cv2.destroyAllWindows()
    exit()


# Constantes útiles
VID_WIDTH = int(videoCapturado.get(cv2.CAP_PROP_FRAME_WIDTH))
VID_HEIGHT = int(videoCapturado.get(cv2.CAP_PROP_FRAME_HEIGHT))
PISO = 942 # Calculado a ojo más o menos donde está la base del cohete (eje X)
ORIGEN = 268 # Calculado a ojo más o menos desde el centro del cohete (eje Y)
FPS = 120

#dataframe donde se guardan posicion,velocidad y aceleracion
dataFrame = pd.DataFrame(data= {'Tiempo (s)':np.array([]),
                                'Posición Y (px)':np.array([])})

# Rastreador CSRT
tracker = cv2.legacy.TrackerCSRT.create()
frame_resized = uv.rescaleFrame(primerFrame, scale=.5)
bbox = cv2.selectROI(frame_resized, False)
tracker.init(frame_resized, bbox)

#comienza a procesar frame por frame:
frame_nro = 0
while True:
    #captura el proximo frame
    exito, frame_actual = videoCapturado.read()
    if not exito:
        break
    frame_resized = uv.rescaleFrame(frame_actual, scale=.5)

    # Actualizar el rastreador
    success, bbox = tracker.update(frame_resized)
    if success:
        x, y, w, h = [int(v) for v in bbox]
        center_x = x + w // 2
        center_y = y + h // 2

        # Guardar las posiciones de acuerdo a nuestro sistema de coordenadas
        final_y = VID_HEIGHT - PISO - (center_y * 2)

        # Calcular el tiempo correspondiente a este fotograma
        time_elapsed = frame_nro / FPS  # Tiempo en segundos

        datos_del_frame = {'Tiempo (s)':[time_elapsed],
             'Posición Y (px)':[final_y]}

        dataFrameAuxiliar = pd.DataFrame(data=datos_del_frame)
        dataFrame = pd.concat([dataFrame, dataFrameAuxiliar], ignore_index=True)

        print(f"Y: {final_y}, Tiempo: {time_elapsed}")

        # Dibujar la caja y el centro
        cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(frame_resized, (center_x, center_y), 5, (0, 0, 255), -1)

    frame_nro += 1

    # Mostrar el fotograma
    cv2.imshow('Tracking', frame_resized)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

videoCapturado.release()
cv2.destroyAllWindows()

#Calcular posición en metros
dataFrame['Posición Y (m)'] = dataFrame['Posición Y (px)'].apply(lambda x: uv.fromPixelsToMeters(x))

def smooth_positions(positions, window_size=10):
    return np.convolve(positions, np.ones(window_size)/window_size, mode='valid')

# Aumentar el tamaño de la ventana (window_size) para suavizar más
smoothed_positions = smooth_positions(dataFrame['Posición Y (m)'], window_size=10)
dataFrame = dataFrame.iloc[:len(smoothed_positions)]
#dataFrame['Posición Y (m)'] = smoothed_positions

periodos =10

# Calcular las velocidades 
dataFrame['Velocidad (m/s)'] = dataFrame['Posición Y (m)'].diff(periods=periodos) / dataFrame['Tiempo (s)'].diff(periods=periodos)	
dataFrame['Velocidad (m/s)'] = dataFrame['Velocidad (m/s)'].fillna(0)

#Calcular la aceleración 
dataFrame['Aceleración (m/s^2)'] = dataFrame['Velocidad (m/s)'].diff(periods=periodos) / dataFrame['Tiempo (s)'].diff(periods=periodos)	
dataFrame['Aceleración (m/s^2)'] = dataFrame['Aceleración (m/s^2)'].fillna(0)

#print(dataFrame)
dataFrame.to_csv('data.csv', index=False)
graficar = input("CSV generado, graficar ahora?(S/N): ")
if(graficar == "s"):
    graficar_csv_plotly(C_POS,C_VEL,C_ACC)
    #graficar_csv_matplot()
    exit()

#Condiciones iniciales de velocidad y posición
v0 = 0
y0 = 0

def velocity(t,g,vo):
  return(g*t+vo)

popt, pcov = curve_fit(velocity, xdata = dataFrame['Tiempo (s)'], ydata = dataFrame['Velocidad (m/s)'], p0 = [9.8, 0])
errs = np.sqrt(np.diag(pcov))
print(popt,errs)