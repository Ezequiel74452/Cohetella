import pandas as pd
import numpy as np
from scipy.optimize import curve_fit


TIEMPO_VEL_FINAL = 2.083


# Función de velocidad
def velocity(t, g):
    return g * t

def position(t, y0, g):
    return y0 + 0.5 * g * t**2

def velocity_caida_libre(t):
    return -9.81 * t

def position_caida_libre(t, y0):
    return y0 + 0.5 * -9.81 * t**2
    
def ajustar_velocidad(dataFrame, dfPtoMaximo):
    
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]

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

def calcular_velocidad_caida_libre(dataFrame, dfPtoMaximo):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    velocidad_caida = velocity_caida_libre(tiempo_ajustado)
    return velocidad_caida

def ajustar_posicion(dataFrame, dfPtoMaximo, g_ajustado):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_ajustada = position(tiempo_ajustado, altura_maxima, g_ajustado)
    return posicion_ajustada

def calcular_posicion_caida_libre(dataFrame, dfPtoMaximo):
    tiempo_pto_maximo = dfPtoMaximo['Tiempo (s)']
    altura_maxima = dfPtoMaximo['Posición Y (m)']
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= tiempo_pto_maximo) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]
    tiempo_ajustado = tiempo_filtrado - tiempo_pto_maximo
    posicion_caida = position_caida_libre(tiempo_ajustado, altura_maxima)
    #Filtrar posiciones mayores a 0
    posicion_caida = posicion_caida[posicion_caida > 0]
    return posicion_caida