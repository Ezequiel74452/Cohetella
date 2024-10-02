import pandas as pd
import numpy as np
from scipy.optimize import curve_fit

TIEMPO_VEL_INICIAL = 0.675
TIEMPO_VEL_FINAL = 2.025
VELOCIDAD_INICIAL = 5.70

# Función de velocidad
def velocity(t, g, vo):
    return g * t + vo

def ajustar_velocidad(dataFrame):
    
    # Filtrar los datos del CSV entre el tiempo donde inicia el lanzamiento y el tiempo donde finaliza el lanzamiento
    tiempo_filtrado = dataFrame['Tiempo (s)'][(dataFrame['Tiempo (s)'] >= TIEMPO_VEL_INICIAL) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]
    velocidad_filtrada = dataFrame['Velocidad (m/s)'][(dataFrame['Tiempo (s)'] >= TIEMPO_VEL_INICIAL) & (dataFrame['Tiempo (s)'] <= TIEMPO_VEL_FINAL)]

    # Ajustar el tiempo para que comience en 0 desde el lanzamiento
    tiempo_ajustado = tiempo_filtrado - TIEMPO_VEL_INICIAL

    # Ajuste de curva de la función de velocidad con los datos filtrados
    popt, pcov = curve_fit(velocity, xdata=tiempo_ajustado, ydata=velocidad_filtrada, p0=[-9.81, VELOCIDAD_INICIAL])
    errs = np.sqrt(np.diag(pcov))

    # Mostrar los parámetros ajustados y sus errores
    print(popt, errs)
    
    g_ajustado, v0_ajustado = popt
    
    velocidad_ajustada = velocity(tiempo_ajustado, g_ajustado, v0_ajustado)
    
    return velocidad_ajustada, tiempo_filtrado