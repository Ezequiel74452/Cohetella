import numpy as np
import math
import pandas as pd
from utils.utilsCaidaLibre import *
from utils.utilsGenerico import *
from utils.utilsTiroOblicuo import *
from utils.utilsTiroVertical import *
from scipy.optimize import curve_fit


LBL_TIEMPO = "Tiempo (s)"
LBL_POS_X = "Posición X (m)"
LBL_POS_Y = "Posición Y (m)"
LBL_VEL_X = "Velocidad X (m/s)"
LBL_VEL_Y = "Velocidad Y (m/s)"
LBL_ACC_X = "Aceleración X (m/s^2)"
LBL_ACC_Y = "Aceleración Y (m/s^2)"

def velocidad_cohete(t, m):
    return -9.8 * t + 7 * np.log(0.73 / m)

def filtrar_df(dataFrame, lower_bound, upper_bound, eje):
	return dataFrame[eje][(dataFrame[LBL_TIEMPO] >= lower_bound) & (dataFrame[LBL_TIEMPO] <= upper_bound)]

def filtrar_inicio_df(dataFrame, tiempo, eje):
	index = (dataFrame[LBL_TIEMPO] - tiempo).abs().idxmin()
	return dataFrame.loc[index][eje]

# ----------------- CÁLCULOS DE CINEMÁTICA LANZAMIENTO VERTICAL-----------------

def calcular_velocidad_vertical(df):
  df['diferencia_posicion'] = df['Posición Y (m)'].shift(-2) - df['Posición Y (m)'].shift(2)
  df['diferencia_tiempoV'] = df['Tiempo (s)'].shift(-2) - df['Tiempo (s)'].shift(2)
  df['Velocidad (m/s)'] = df['diferencia_posicion'] / df['diferencia_tiempoV']
  df['Velocidad (m/s)'] = df['Velocidad (m/s)'].fillna(0)
  df.drop(['diferencia_posicion', 'diferencia_tiempoV'], axis=1, inplace=True)
  return df

def calcular_aceleracion_vertical(df):
  df['diferencia_velocidad'] = df['Velocidad (m/s)'].shift(-2) - df['Velocidad (m/s)'].shift(2)
  df['diferencia_tiempoA'] = df['Tiempo (s)'].shift(-2) - df['Tiempo (s)'].shift(2)
  df['Aceleración (m/s^2)'] = df['diferencia_velocidad'] / df['diferencia_tiempoA']
  df['Aceleración (m/s^2)'] = df['Aceleración (m/s^2)'].fillna(0)
  df.drop(['diferencia_velocidad', 'diferencia_tiempoA'], axis=1, inplace=True)
  return df

def alturaMaximaInicio(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[0]

def alturaMaximaFin(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[-1]

def puntoMedioAlturaMaxima(df: pd.DataFrame):
    inicio = alturaMaximaInicio(df)
    fin = alturaMaximaFin(df)
    indice_inicio = df.index[df['Posición Y (m)'] == inicio['Posición Y (m)']][0]
    indice_fin = df.index[df['Posición Y (m)'] == fin['Posición Y (m)']][-1]
    
    indice_medio = (indice_inicio + indice_fin) // 2
    return df.iloc[indice_medio]

def calcularVelocidadMaximaInicial(df: pd.DataFrame):
	vel_max_incial = df['Velocidad (m/s)'].max()
	return df[df['Velocidad (m/s)'] == vel_max_incial].iloc[-1]

def calcularVelocidadMaximaFinal(df: pd.DataFrame):
	vel_max_final = df['Velocidad (m/s)'].min()
	return df[df['Velocidad (m/s)'] == vel_max_final].iloc[-1]

# ----------------- AJUSTAR VELOCIDAD A ECUACIÓN DE CAÍDA LIBRE -----------------

def ajustar_velocidad_CL(dataFrame, dfPtoMaximo, dfVelMaxFinal):
    
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]

    # Ajustar el tiempo para que comience en 0 desde el lanzamiento
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo

    # Ajuste de curva de la función de velocidad con los datos filtrados
    popt, pcov = curve_fit(velocity, xdata=tiempo_ajustado, ydata=velocidad_filtrada, p0=[-9.81])
    errs = np.sqrt(np.diag(pcov))

    # Mostrar los parámetros ajustados y sus errores
    print(popt, errs)
    
    g_ajustado = popt[0]
    err_g= errs[0] 
    
    velocidad_ajustada = velocity(tiempo_ajustado, g_ajustado)
    
    return velocidad_ajustada, tiempo_filtrado, g_ajustado, err_g

# ----------------- CALCULAR VELOCIDAD CAÍDA LIBRE -----------------

def calcular_velocidad_caida_libre(dataFrame, dfPtoMaximo, dfVelMaxFinal):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    velocidad_caida = velocity_caida_libre(tiempo_ajustado)
    return velocidad_caida
  
# ----------------- AJUSTAR POSICIÓN A ECUACIÓN DE CAÍDA LIBRE -----------------

def ajustar_posicion_CL(dataFrame, dfPtoMaximo, dfVelMaxFinal, g_ajustado):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_ajustada = position(tiempo_ajustado, altura_maxima, g_ajustado)
    return posicion_ajustada

# ----------------- CALCULAR POSICIÓN CAÍDA LIBRE -----------------
def calcular_posicion_caida_libre(dataFrame, dfPtoMaximo, dfVelMaxFinal):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_caida = position_caida_libre(tiempo_ajustado, altura_maxima)
    posicion_caida = posicion_caida[posicion_caida > 0]
    return posicion_caida

# ----------------- AJUSTAR VELOCIDAD A ECUACIÓN DE TIRO VERTICAL -----------------
def ajustar_velocidad_TV(dataFrame, dfVelMaxInicial, dfVelMaxFinal):
    
    tiempo_vel_maxima_inicial = dfVelMaxInicial['Tiempo (s)']
    vel_maxima_inicial = dfVelMaxInicial['Velocidad (m/s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima_inicial) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima_inicial) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]

    # Ajustar el tiempo para que comience en 0 desde el lanzamiento
    tiempo_ajustado = tiempo_filtrado -  tiempo_vel_maxima_inicial

    # Ajuste de curva de la función de velocidad con los datos filtrados
    popt, pcov = curve_fit(velocity, xdata=tiempo_ajustado, ydata=velocidad_filtrada, p0=[-9.81, vel_maxima_inicial])
    errs = np.sqrt(np.diag(pcov))

    # Mostrar los parámetros ajustados y sus errores
    print(popt, errs)
    
    g_ajustado = popt[0]
    err_g= errs[0]
    
    velocidad_ajustada = velocity(tiempo_ajustado, g_ajustado, vel_maxima_inicial)
    
    return velocidad_ajustada, tiempo_filtrado, g_ajustado, err_g
  
# ----------------- CALCULAR VELOCIDAD TIRO VERTICAL -----------------

def calcular_velocidad_tiro_vertical(dataFrame, dfVelMaxInicial, dfVelMaxFinal):
    tiempo_vel_maxima_inicial = dfVelMaxInicial['Tiempo (s)']
    vel_maxima_inicial = dfVelMaxInicial['Velocidad (m/s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima_inicial) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima_inicial
    velocidad_tiro_vertical = velocity_tiro_vertical(tiempo_ajustado, vel_maxima_inicial)
    return velocidad_tiro_vertical

# ----------------- AJUSTAR POSICIÓN A ECUACIÓN DE TIRO VERTICAL -----------------

def ajustar_posicion_TV(dataFrame, dfVelMaxInicial, dfVelMaxFinal, g_ajustado):
    tiempo_vel_maxima_inicial = dfVelMaxInicial['Tiempo (s)']
    vel_maxima_inicial = dfVelMaxInicial['Velocidad (m/s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    altura_inicial = dfVelMaxInicial['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima_inicial) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima_inicial
    posicion_ajustada = position(tiempo_ajustado, altura_inicial, g_ajustado, vel_maxima_inicial)
    return posicion_ajustada

# ----------------- CALCULAR POSICION TIRO VERTICAL -----------------

def calcular_posicion_tiro_vertical(dataFrame, dfVelMaxInicial, dfVelMaxFinal):
    tiempo_vel_maxima_inicial = dfVelMaxInicial['Tiempo (s)']
    vel_maxima_inicial = dfVelMaxInicial['Velocidad (m/s)']
    tiempo_vel_maxima_final = dfVelMaxFinal['Tiempo (s)']
    altura_inicial = dfVelMaxInicial['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima_inicial) & (dataFrame['Tiempo (s)'] <= tiempo_vel_maxima_final)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima_inicial
    posicion_tiro_vertical = position_tiro_vertical(tiempo_ajustado, altura_inicial, vel_maxima_inicial)
    posicion_tiro_vertical = posicion_tiro_vertical[posicion_tiro_vertical > 0]
    return posicion_tiro_vertical
  

def calcular_velocidad_exp(dataFrame, dfTiempoLanzamiento, dfTiempoAterrizaje):
    tiempo_lanzamiento = dfTiempoLanzamiento['Tiempo (s)']
    tiempo_aterrizaje = dfTiempoAterrizaje['Tiempo (s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_lanzamiento) & (dataFrame['Tiempo (s)'] <= tiempo_aterrizaje)]
    
    tiempo_ajustado = tiempo_filtrado - tiempo_lanzamiento
    masa_filtrada = dataFrame['Masa (kg)'][(dataFrame['Tiempo (s)'] >= tiempo_lanzamiento) & (dataFrame['Tiempo (s)'] <= tiempo_aterrizaje)]
    print(f"masa filtrada: {masa_filtrada}, tiempo ajustado: {tiempo_ajustado}")
    velocidad_exp = velocidad_cohete(tiempo_ajustado, masa_filtrada)
    return velocidad_exp, tiempo_filtrado

# ----------------- CÁLCULOS DE CINEMÁTICA LANZAMIENTO OBLICUO -----------------

# Tiempos velocidad máxima
TIEMPO_VEL_MAXIMA_OBLIQUE = 2.1875
TIEMPO_VEL_FINAL_OBLIQUE = 3.88  

def calcular_velocidad_oblicuo(df):
  df['diferencia_posicion_x'] = df['Posición X (m)'].shift(-5) - df['Posición X (m)'].shift(5)
  df['diferencia_posicion_y'] = df['Posición Y (m)'].shift(-5) - df['Posición Y (m)'].shift(5)
  df['diferencia_tiempoV'] = df['Tiempo (s)'].shift(-5) - df['Tiempo (s)'].shift(5)
  df['Velocidad X (m/s)'] = df['diferencia_posicion_x'] / df['diferencia_tiempoV']
  df['Velocidad Y (m/s)'] = df['diferencia_posicion_y'] / df['diferencia_tiempoV']
  df['Velocidad X (m/s)'] = df['Velocidad X (m/s)'].fillna(0)
  df['Velocidad Y (m/s)'] = df['Velocidad Y (m/s)'].fillna(0)
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

def calcularVelocidadMaximaInicialObliqueX(df: pd.DataFrame):
	vel_max_incial = df['Velocidad X (m/s)'].max()
	return df[df['Velocidad X (m/s)'] == vel_max_incial].iloc[-1]

def calcularVelocidadMaximaInicialObliqueY(df: pd.DataFrame):
	vel_max_incial = df['Velocidad Y (m/s)'].max()
	return df[df['Velocidad Y (m/s)'] == vel_max_incial].iloc[-1]

def calcularVelocidadMaximaFinalOblique(df: pd.DataFrame):
	vel_max_final = df['Velocidad Y (m/s)'].min()
	return df[df['Velocidad Y (m/s)'] == vel_max_final].iloc[-1]

# ----------------- AJUSTAR POSICIÓN OBLICUA -----------------

def ajustar_posicion_oblique_x(dataFrame, g_ajustado_x):
	tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
	pos_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_POS_X)
	vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_X)

	tiempo_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
	tiempo_ajustado = tiempo_filtrado - tiempo_despegue
	posicion_ajustada = position_oblique_x(tiempo_ajustado, pos_inicial, g_ajustado_x, vel_inicial)
	return posicion_ajustada

def ajustar_posicion_oblique_y(dataFrame, g_ajustado_y):
  tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
  pos_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_POS_Y)
  vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_X)
  
  tiempo_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
  tiempo_ajustado = tiempo_filtrado - tiempo_despegue
  posicion_ajustada = position_oblique_y(tiempo_ajustado, pos_inicial, g_ajustado_y, vel_inicial)
  return posicion_ajustada

# ----------------- CALCULAR POSICIÓN OBLICUA -----------------

def calcular_posicion_oblique_x(dataFrame):
  tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
  pos_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_POS_X)
  vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_X)
  
  tiempo_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
  tiempo_ajustado = tiempo_filtrado - tiempo_despegue
  
  posicion_tiro_oblicuo = pos_oblique_x(tiempo_ajustado, pos_inicial, vel_inicial)
  posicion_tiro_oblicuo = posicion_tiro_oblicuo[posicion_tiro_oblicuo > 0]
  return posicion_tiro_oblicuo

def calcular_posicion_oblique_y(dataFrame):
  tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
  pos_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_POS_Y)
  vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_Y)
  
  tiempo_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
  tiempo_ajustado = tiempo_filtrado - tiempo_despegue
  
  posicion_tiro_oblicuo = pos_oblique_y(tiempo_ajustado, pos_inicial, vel_inicial)
  posicion_tiro_oblicuo = posicion_tiro_oblicuo[posicion_tiro_oblicuo > 0]
  return posicion_tiro_oblicuo

# ----------------- AJUSTAR VELOCIDAD OBLICUA -----------------

def ajustar_velocidad_oblique_x(dataFrame):
	tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
	vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_X)

	tiempo_despegue_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
	velocidad_filtrada_X = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_VEL_X)

	tiempo_despegue_ajustado = tiempo_despegue_filtrado - tiempo_despegue

	popt_x, pcov_x = curve_fit(velocity_oblique_x,
														xdata=tiempo_despegue_ajustado,
                            ydata=velocidad_filtrada_X,
                            p0=[0])
	"""popt_x, pcov_x = curve_fit(velocity_oblique_x,
														xdata=tiempo_despegue_ajustado,
                            ydata=velocidad_filtrada_X,
                            p0=[0, vel_inicial])"""
	errs_x = np.sqrt(np.diag(pcov_x))

	print(f"Popt_x: {popt_x}")
	print(f"Pcov_x: {pcov_x}")
	print(f"Errs_x: {errs_x}")

	#vel_ajustada = popt_x[1]
	g_ajustado_x = popt_x[0]

	err_g_x = errs_x[0]

	#velocidad_ajustada_x = velocity_oblique_x(tiempo_despegue_ajustado, g_ajustado_x, vel_ajustada)
	#velocidad_ajustada_x = velocity_oblique_x(tiempo_despegue_ajustado, g_ajustado_x, vel_inicial)
	velocidad_ajustada_x = velocity_oblique_x(tiempo_despegue_ajustado, g_ajustado_x)

	return velocidad_ajustada_x, tiempo_despegue_filtrado, g_ajustado_x, err_g_x
	#return velocidad_ajustada_x, tiempo_despegue_filtrado, g_ajustado_x, err_g_x, vel_ajustada

def ajustar_velocidad_oblique_y(dataFrame):
	tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
	vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_Y)

	tiempo_despegue_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
	velocidad_filtrada_Y = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_VEL_Y)

	tiempo_despegue_ajustado = tiempo_despegue_filtrado - tiempo_despegue
	popt_y, pcov_y = curve_fit(velocity_oblique_y,
                            xdata=tiempo_despegue_ajustado,
                            ydata=velocidad_filtrada_Y,
                            p0=[-9.81])
	"""popt_y, pcov_y = curve_fit(velocity_oblique_y,
                            xdata=tiempo_despegue_ajustado,
                            ydata=velocidad_filtrada_Y,
                            p0=[-9.81, vel_inicial])"""
	errs_y = np.sqrt(np.diag(pcov_y))

	print(f"Popt_y: {popt_y}")
	print(f"Pcov_y: {pcov_y}")
	print(f"Errs_y: {errs_y}")

	#vel_ajustada = popt_y[1]
	g_ajustado_y = popt_y[0]

	err_g_y = errs_y[0]
	
	#velocidad_ajustada_y = velocity_oblique_y(tiempo_despegue_ajustado, g_ajustado_y, vel_ajustada)
	#velocidad_ajustada_y = velocity_oblique_y(tiempo_despegue_ajustado, g_ajustado_y, vel_inicial)
	velocidad_ajustada_y = velocity_oblique_y(tiempo_despegue_ajustado, g_ajustado_y)
  
	return velocidad_ajustada_y, tiempo_despegue_filtrado, g_ajustado_y, err_g_y
	#return velocidad_ajustada_y,tiempo_despegue_filtrado, g_ajustado_y, err_g_y, vel_ajustada

# ----------------- CALCULAR VELOCIDAD OBLICUA -----------------

def calcular_velocidad_oblique_x(dataFrame):
	tiempo_vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
	vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_X)

	tiempo_filtrado = filtrar_df(dataFrame, tiempo_vel_inicial, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
	tiempo_ajustado = tiempo_filtrado - tiempo_vel_inicial

	velocidad_oblique_x = vel_oblique_x(tiempo_ajustado, vel_inicial)
	return velocidad_oblique_x

def calcular_velocidad_oblique_y(dataFrame):
  tiempo_vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_TIEMPO)
  vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE, LBL_VEL_Y)
  
  tiempo_filtrado = filtrar_df(dataFrame, tiempo_vel_inicial, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
  tiempo_ajustado = tiempo_filtrado - tiempo_vel_inicial
  
  velocidad_oblique_y = vel_oblique_y(tiempo_ajustado, vel_inicial)
  return velocidad_oblique_y