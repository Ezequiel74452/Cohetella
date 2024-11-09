import numpy as np
import math
import pandas as pd
from utils.utilsCaidaLibre import *
from utils.utilsGenerico import *
from utils.utilsTiroOblicuo import *
from utils.utilsTiroVertical import *
from scipy.optimize import curve_fit

TIEMPO_VEL_FINAL_VERTICAL = 2.083
# Tiempos al momento de despegar
#TIEMPO_DESPEGUE_OBLIQUE_X = 1.954
#TIEMPO_DESPEGUE_OBLIQUE_Y = 1.958

# Tiempos velocidad máxima
TIEMPO_VEL_MAXIMA_OBLIQUE = 2.1875
TIEMPO_VEL_FINAL_OBLIQUE = 3.88

LBL_TIEMPO = "Tiempo (s)"
LBL_POS_X = "Posición X (m)"
LBL_POS_Y = "Posición Y (m)"
LBL_VEL_X = "Velocidad X (m/s)"
LBL_VEL_Y = "Velocidad Y (m/s)"
LBL_ACC_X = "Aceleración X (m/s^2)"
LBL_ACC_Y = "Aceleración Y (m/s^2)"

def filtrar_df(dataFrame, lower_bound, upper_bound, eje):
	return dataFrame[eje][(dataFrame[LBL_TIEMPO] >= lower_bound) & (dataFrame[LBL_TIEMPO] <= upper_bound)]

def filtrar_inicio_df(dataFrame, tiempo, eje):
	index = (dataFrame[LBL_TIEMPO] - tiempo).abs().idxmin()
	return dataFrame.loc[index][eje]

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

# ----------------- AJUSTAR VELOCIDAD CAÍDA LIBRE -----------------

def ajustar_velocidad_CL(dataFrame, dfPtoMaximo):
    
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]

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

def calcular_velocidad_caida_libre(dataFrame, dfPtoMaximo):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_OBLIQUE)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    velocidad_caida = velocity_caida_libre(tiempo_ajustado)
    return velocidad_caida

def ajustar_posicion_CL(dataFrame, dfPtoMaximo, g_ajustado):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_OBLIQUE)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_ajustada = position(tiempo_ajustado, altura_maxima, g_ajustado)
    return posicion_ajustada

def calcular_posicion_caida_libre(dataFrame, dfPtoMaximo):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_OBLIQUE)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_caida = position_caida_libre(tiempo_ajustado, altura_maxima)
    #Filtrar posiciones mayores a 0
    posicion_caida = posicion_caida[posicion_caida > 0]
    return posicion_caida

def ajustar_velocidad_TV(dataFrame, dfVelMaxima):
    print(dfVelMaxima)
    
    tiempo_vel_maxima = dfVelMaxima['Tiempo (s)']
    vel_maxima = dfVelMaxima['Velocidad (m/s)']
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]

    # Ajustar el tiempo para que comience en 0 desde el lanzamiento
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima

    # Ajuste de curva de la función de velocidad con los datos filtrados
    popt, pcov = curve_fit(velocity, xdata=tiempo_ajustado, ydata=velocidad_filtrada, p0=[-9.81, vel_maxima])
    errs = np.sqrt(np.diag(pcov))

    # Mostrar los parámetros ajustados y sus errores
    print(popt, errs)
    
    g_ajustado = popt[0]
    err_g= errs[0]
    
    velocidad_ajustada = velocity(tiempo_ajustado, g_ajustado, vel_maxima)
    
    return velocidad_ajustada, tiempo_filtrado, g_ajustado, err_g

def calcular_velocidad_tiro_vertical(dataFrame, dfVelMaxima):
    tiempo_vel_maxima = dfVelMaxima['Tiempo (s)']
    vel_maxima = dfVelMaxima['Velocidad (m/s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima
    velocidad_tiro_vertical = velocity_tiro_vertical(tiempo_ajustado, vel_maxima)
    return velocidad_tiro_vertical

def ajustar_posicion_TV(dataFrame, dfVelMaxima, g_ajustado):
    tiempo_vel_maxima = dfVelMaxima['Tiempo (s)']
    vel_maxima = dfVelMaxima['Velocidad (m/s)']
    altura_inicial = dfVelMaxima['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima
    posicion_ajustada = position(tiempo_ajustado, altura_inicial, g_ajustado, vel_maxima)
    return posicion_ajustada

def calcular_posicion_tiro_vertical(dataFrame, dfVelMaxima):
    tiempo_vel_maxima = dfVelMaxima['Tiempo (s)']
    vel_maxima = dfVelMaxima['Velocidad (m/s)']
    altura_inicial = dfVelMaxima['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_vel_maxima) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL_VERTICAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_vel_maxima
    posicion_tiro_vertical = position_tiro_vertical(tiempo_ajustado, altura_inicial, vel_maxima)
    posicion_tiro_vertical = posicion_tiro_vertical[posicion_tiro_vertical > 0]
    return posicion_tiro_vertical