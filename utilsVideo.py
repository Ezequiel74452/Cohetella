import cv2
import numpy as np

PX_TO_CM = 0.64286
PX_TO_CM_OBLICUO = 0.9047
TIEMPO_LANZAMIENTO = 0.475
TIEMPO_ALTURA_MAXIMA = 1.225
TIEMPO_ENTRE_LANZ_ALTMAX = 1.225 - 0.475

def rescaleFrame(frame, scale=0.75):
  width = frame.shape[1] * scale
  height = frame.shape[0] * scale
  dimensions = (int(width), int(height))
  return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def fromPixelsToMeters(x):
  return x * PX_TO_CM / 100

def fromPixelsToMetersOblicuo(x):
  return x * PX_TO_CM_OBLICUO / 100

def masaConRespectoAlTiempo(t):
    # Calcular la pendiente de disminución de la masa
    pendiente = (0.03 - 0.73) / (TIEMPO_ALTURA_MAXIMA - TIEMPO_LANZAMIENTO)
    
    # Utilizar np.where para hacer comparaciones vectorizadas con los tiempos dados
    return np.where(t < TIEMPO_LANZAMIENTO, 0.73,  # Antes del lanzamiento
                    np.where(t > TIEMPO_ALTURA_MAXIMA, 0.03,  # Después de la altura máxima
                             0.73 + pendiente * (t - TIEMPO_LANZAMIENTO)))  # Durante el ascenso

def smooth_positions(positions, window_size=10):
	return np.convolve(positions, np.ones(window_size)/window_size, mode='valid')

def posicion_en_metros_vertical(df):
  df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: fromPixelsToMeters(x))
  return df

def posicion_en_metros_oblicuo(df):
	df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: fromPixelsToMetersOblicuo(x))
	df['Posición X (m)'] = df['Posición X (px)'].apply(lambda x: fromPixelsToMetersOblicuo(x))
	return df

def suavizar_df_vertical(df):
  smoothed_positions = smooth_positions(df['Posición Y (m)'], window_size=10)
  df = df.iloc[:len(smoothed_positions)]
  return df

def suavizar_df_oblicuo(df):
  smoothed_positions_y = smooth_positions(df['Posición Y (m)'], window_size=10)
  smoothed_positions_x = smooth_positions(df['Posición X (m)'], window_size=10)
  df = df.iloc[:len(smoothed_positions_y)]
  df['Posición Y (m)'] = smoothed_positions_y
  df['Posición X (m)'] = smoothed_positions_x
  return df

def calcular_velocidad_vertical(df):
    # Calcular la diferencia de posición y tiempo con un desplazamiento de 5
    df['diferencia_posicion'] = df['Posición Y (m)'].shift(-5) - df['Posición Y (m)'].shift(5)
    df['diferencia_tiempoV'] = df['Tiempo (s)'].shift(-5) - df['Tiempo (s)'].shift(5)
    
    # Calcular la velocidad dividiendo las diferencias
    df['Velocidad (m/s)'] = df['diferencia_posicion'] / df['diferencia_tiempoV']
    
    # Rellenar valores NaN con 0 en la columna de velocidad
    df['Velocidad (m/s)'] = df['Velocidad (m/s)'].fillna(0)
    
    return df


def calcular_velocidad_oblicuo(df):
  df['diferencia_posicion_x'] = df['Posición X (m)'].shift(-5) - df['Posición X (m)'].shift(5)
  df['diferencia_posicion_y'] = df['Posición Y (m)'].shift(-5) - df['Posición Y (m)'].shift(5)
  df['diferencia_tiempoV'] = df['Tiempo (s)'].shift(-5) - df['Tiempo (s)'].shift(5)
  df['Velocidad X (m/s)'] = df['diferencia_posicion_x'] / df['diferencia_tiempoV']
  df['Velocidad Y (m/s)'] = df['diferencia_posicion_y'] / df['diferencia_tiempoV']
  df['Velocidad X (m/s)'] = df['Velocidad X (m/s)'].fillna(0)
  df['Velocidad Y (m/s)'] = df['Velocidad Y (m/s)'].fillna(0)
  return df

def calcular_aceleracion_vertical(df):
  df['diferencia_velocidad'] = df['Velocidad (m/s)'].shift(-5) - df['Velocidad (m/s)'].shift(5)
  df['diferencia_tiempoA'] = df['Tiempo (s)'].shift(-5) - df['Tiempo (s)'].shift(5)
  df['Aceleración (m/s^2)'] = df['diferencia_velocidad'] / df['diferencia_tiempoA']
  df['Aceleración (m/s^2)'] = df['Aceleración (m/s^2)'].fillna(0)
  return df

def calcular_aceleracion_oblicuo(df):
  df['diferencia_velocidad_x'] = df['Velocidad X (m/s)'].shift(-5) - df['Velocidad X (m/s)'].shift(5)
  df['diferencia_velocidad_y'] = df['Velocidad Y (m/s)'].shift(-5) - df['Velocidad Y (m/s)'].shift(5)
  df['diferencia_tiempoA'] = df['Tiempo (s)'].shift(-5) - df['Tiempo (s)'].shift(5)
  df['Aceleración X (m/s^2)'] = df['diferencia_velocidad_x'] / df['diferencia_tiempoA']
  df['Aceleración Y (m/s^2)'] = df['diferencia_velocidad_y'] / df['diferencia_tiempoA']
  df['Aceleración X (m/s^2)'] = df['Aceleración X (m/s^2)'].fillna(0)
  df['Aceleración Y (m/s^2)'] = df['Aceleración Y (m/s^2)'].fillna(0)
  return df

def calcular_masa_vertical(df):
    
    # Calcular las masas con respecto al tiempo ajustado
    df['Masa (kg)'] = masaConRespectoAlTiempo(df['Tiempo (s)'])    
    # Reemplazar NaN en las filas que no tienen valores de masa por 0
    df['Masa (kg)'] = df['Masa (kg)'].fillna(0)  
    return df

def calcular_cantidad_movimiento(df):
  df['Cantidad de Movimiento'] = df['Velocidad (m/s)'] * df['Masa (kg)']
  return df 

def calcular_fuerza(df):
  df['diferencia_cantidad_movimiento'] = df['Cantidad de Movimiento'].shift(-3) - df['Cantidad de Movimiento'].shift(3)
  df['diferencia_tiempoCM'] = df['Tiempo (s)'].shift(-3) - df['Tiempo (s)'].shift(3)
  df['Fuerza (N)'] = df['diferencia_cantidad_movimiento'] / df['diferencia_tiempoCM']
  df['Fuerza (N)'] = df['Fuerza (N)'].fillna(0)
  return df