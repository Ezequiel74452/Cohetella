import cv2
import numpy as np

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
	return df

def calcular_velocidad_vertical(df):
	df['Velocidad (m/s)'] = df['Posición Y (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
	df['Velocidad (m/s)'] = df['Velocidad (m/s)'].fillna(0)
	return df

def calcular_velocidad_oblicuo(df):
  df['Velocidad Y (m/s)'] = df['Posición Y (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)
  df['Velocidad Y (m/s)'] = df['Velocidad Y (m/s)'].fillna(0)
  df['Velocidad X (m/s)'] = df['Posición X (m)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)
  df['Velocidad X (m/s)'] = df['Velocidad X (m/s)'].fillna(0)
  return df

def calcular_aceleracion_vertical(df):
  df['Aceleración (m/s^2)'] = df['Velocidad (m/s)'].diff(periods=10) / df['Tiempo (s)'].diff(periods=10)	
  df['Aceleración (m/s^2)'] = df['Aceleración (m/s^2)'].fillna(0)
  return df

def calcular_aceleracion_oblicuo(df):
	df['Aceleración Y (m/s^2)'] = df['Velocidad Y (m/s)'].diff(periods=5) / df['Tiempo (s)'].diff(periods=5)
	df['Aceleración Y (m/s^2)'] = df['Aceleración Y (m/s^2)'].fillna(0)
	df['Aceleración X (m/s^2)'] = df['Velocidad X (m/s)'].diff(periods=5) / df['Tiempo (s)'].diff(periods=5)
	df['Aceleración X (m/s^2)'] = df['Aceleración X (m/s^2)'].fillna(0)
	return df