import numpy as np


def masaConRespectoAlTiempo(t, tiempo_lanzamiento, tiempo_velocidad_maxima_inicial):
    # Calcular la pendiente de disminución de la masa
    pendiente = (0.03 - 0.73) / (tiempo_velocidad_maxima_inicial - tiempo_lanzamiento)
    
    # Utilizar np.where para hacer comparaciones vectorizadas con los tiempos dados
    return np.where(t < tiempo_lanzamiento, 0.73,  # Antes del lanzamiento
                    np.where(t > tiempo_velocidad_maxima_inicial, 0.03,  # Después de la altura máxima
										0.73 + pendiente * (t - tiempo_lanzamiento)))  # Durante el ascenso


def calcular_masa_vertical(df, df_tiempo_lanzamiento, df_tiempo_velocidad_maxima_inicial):
  tiempo_lanzamiento = df_tiempo_lanzamiento['Tiempo (s)']
  tiempo_velocidad_maxima_inicial = df_tiempo_velocidad_maxima_inicial['Tiempo (s)']
  df['Masa (kg)'] = masaConRespectoAlTiempo(df['Tiempo (s)'], tiempo_lanzamiento, tiempo_velocidad_maxima_inicial)
  df['Masa (kg)'] = df['Masa (kg)'].fillna(0)  
  return df

def calcular_cantidad_movimiento(df):
  df['Cantidad de Movimiento'] = df['Velocidad (m/s)'] * df['Masa (kg)']
  return df 

def calcular_fuerza(df):
  df['Fuerza (N)'] = df['Masa (kg)'] * df['Aceleración (m/s^2)']
  df['Fuerza (N)'] = df['Fuerza (N)'].fillna(0)
  
  df['Peso (N)'] = df['Masa (kg)'] * -9.81
  
  return df

def calcular_rozamiento_viscoso(df, df_tiempo_altura_maxima, df_tiempo_aterrizaje):
  tiempo_altura_maxima = df_tiempo_altura_maxima['Tiempo (s)'] + 0.1
  tiempo_aterrizaje = df_tiempo_aterrizaje['Tiempo (s)'] - 0.1
  df.loc[(df['Tiempo (s)'] >= tiempo_altura_maxima) & (df['Tiempo (s)'] <= tiempo_aterrizaje), 'Rozamiento viscoso (N)'] = (
		df['Masa (kg)'] * (9.81 + df['Aceleración (m/s^2)'])
  )
  return df