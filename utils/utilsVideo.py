import cv2
import numpy as np
from scipy.ndimage import gaussian_filter1d

PX_TO_CM = 0.64286
PX_TO_CM_OBLICUO = 0.9047

def rescaleFrame(frame, scale=0.75):
  width = frame.shape[1] * scale
  height = frame.shape[0] * scale
  dimensions = (int(width), int(height))
  return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def fromPixelsToMeters(x):
  return x * PX_TO_CM / 100

def fromPixelsToMetersOblicuo(x):
  return x * PX_TO_CM_OBLICUO / 100


def posicion_en_metros_vertical(df):
  df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: fromPixelsToMeters(x))
  return df

def posicion_en_metros_oblicuo(df):
	df['Posición Y (m)'] = df['Posición Y (px)'].apply(lambda x: fromPixelsToMetersOblicuo(x))
	df['Posición X (m)'] = df['Posición X (px)'].apply(lambda x: fromPixelsToMetersOblicuo(x))
	return df

def suavizar_df_vertical(df):
  smoothed_positions = gaussian_filter1d(df['Posición Y (m)'], sigma=4)
  df = df.iloc[:len(smoothed_positions)]
  df['Posición Y (m)'] = smoothed_positions
  return df

def suavizar_df_oblicuo(df):
  smoothed_positions_y = gaussian_filter1d(df['Posición Y (m)'], sigma=2)
  smoothed_positions_x = gaussian_filter1d(df['Posición X (m)'], sigma=2)
  df = df.iloc[:len(smoothed_positions_y)]
  df['Posición Y (m)'] = smoothed_positions_y
  df['Posición X (m)'] = smoothed_positions_x
  return df

def calcular_tiempo_lanzamiento(df, vel_threshold=0.3):
  lanzamiento_idx = np.where(df['Velocidad (m/s)'] > vel_threshold)[0][0]
  return df.iloc[lanzamiento_idx]

def calcular_tiempo_aterrizaje(df, dfTiempoVelMaxFinal, vel_max_threshold=-0.5, altura_umbral=0.3):
    indices_aterrizaje = np.where(
        (df['Velocidad (m/s)'] > vel_max_threshold) & 
        (df['Tiempo (s)'] > dfTiempoVelMaxFinal['Tiempo (s)']) &
        (np.abs(df['Posición Y (m)']) < altura_umbral)
    )[0]
    
    if len(indices_aterrizaje) > 0:
        aterrizaje_idx = indices_aterrizaje[0]
        return df.iloc[aterrizaje_idx]
    else:
        return None  