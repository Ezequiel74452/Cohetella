import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import webbrowser
from scipy.optimize import curve_fit
from sympy import *
from utilsGraficas import oblique_graph, graficar_oblique_csv_plotly

"""CSV_PATH = "oblicuo120fps.csv"

def principal_oblique():
	path_to_html = graficar_oblique_csv_plotly()
	file_url = 'file://' + os.path.abspath(path_to_html).replace('\\', '/')
	webbrowser.open(file_url)

def principal_vertical():
	df = pd.read_csv(CSV_PATH)
	#path_to_html = oblique_graph(df)
	#file_url = 'file://' + os.path.abspath(path_to_html).replace('\\', '/')
	#webbrowser.open(file_url)
	df = df.dropna().copy() # Elimino las filas que tienen NaNs
	popt, pcov = curve_fit(velocity, xdata = df["Tiempo (s)"], ydata = df["Velocidad Y (m/s)"])
	errs = np.sqrt(np.diag(pcov))
	print(popt,errs)
	fig = go.Figure()
	fig.add_traces(go.Scatter(x = df["Tiempo (s)"], y = df["Velocidad Y (m/s)"], mode = 'markers'))
	fig.add_traces(go.Scatter(x = df["Tiempo (s)"], y = velocity(df["Tiempo (s)"],popt[0],popt[1])))

def velocity(t,g,vo):
  return(g*t+vo)

if __name__ == "__main__":
	principal_vertical()"""

import pandas as pd

TIEMPO_VEL_FINAL_VERTICAL = 2.083
# Tiempos al momento de despegar
TIEMPO_DESPEGUE_OBLIQUE_X = 1.954
TIEMPO_DESPEGUE_OBLIQUE_Y = 1.958

# Tiempos velocidad máxima
TIEMPO_VEL_MAXIMA_OBLIQUE_X = 2.1785
TIEMPO_VEL_MAXIMA_OBLIQUE_Y = 2.1785
TIEMPO_VEL_FINAL_OBLIQUE = 3.88

LBL_TIEMPO = "Tiempo (s)"
LBL_POS_X = "Posición X (m)"
LBL_POS_Y = "Posición Y (m)"
LBL_VEL_X = "Velocidad X (m/s)"
LBL_VEL_Y = "Velocidad Y (m/s)"
LBL_ACC_X = "Aceleración X (m/s^2)"
LBL_ACC_Y = "Aceleración Y (m/s^2)"

def velocity_oblique_x(t, g, v0=0):
    return v0 + g * t

def filtrar_df(dataFrame, lower_bound, upper_bound, eje):
	return dataFrame[eje][(dataFrame[LBL_TIEMPO] >= lower_bound) & (dataFrame[LBL_TIEMPO] <= upper_bound)]

def filtrar_inicio_df(dataFrame, tiempo, eje):
	index = (dataFrame[LBL_TIEMPO] - tiempo).abs().idxmin()
	return dataFrame.loc[index][eje]

def ajustar_velocidad_oblique_x(dataFrame):
	tiempo_despegue = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE_X, LBL_TIEMPO)
	tiempo_vel_max = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE_X, LBL_TIEMPO)
	vel_inicial = filtrar_inicio_df(dataFrame, TIEMPO_VEL_MAXIMA_OBLIQUE_X, LBL_VEL_X)

	tiempo_filtrado = filtrar_df(dataFrame, tiempo_despegue, TIEMPO_VEL_FINAL_OBLIQUE, LBL_TIEMPO)
	print(f"Tiempo filtrado:\n {tiempo_filtrado}")
	velocidad_filtrada_X = filtrar_df(dataFrame, tiempo_vel_max, TIEMPO_VEL_FINAL_OBLIQUE, LBL_VEL_X)
	print(f"Velocidad filtrada:\n {velocidad_filtrada_X}")
	velocidad_filtrada_X = velocidad_filtrada_X.reindex(range(len(tiempo_filtrado)), method='ffill')

	tiempo_ajustado = tiempo_filtrado - tiempo_despegue
	print(f"Tiempo ajustado:\n {tiempo_ajustado}")
	print(f"Velocidad filtrada final:\n {velocidad_filtrada_X}")

	popt_x, pcov_x = curve_fit(velocity_oblique_x,
														xdata=tiempo_ajustado,
                            ydata=velocidad_filtrada_X,
                            p0=[0])
	errs_x = np.sqrt(np.diag(pcov_x))

	g_ajustado_x = popt_x[0]

	err_g_x = errs_x[0]

	velocidad_ajustada_x = velocity_oblique_x(tiempo_ajustado, g_ajustado_x, vel_inicial)

	return velocidad_ajustada_x, tiempo_filtrado, g_ajustado_x, err_g_x

dataFrame = pd.read_csv("oblicuo240fps.csv")
vel_ajustada, tiempo, g, err = ajustar_velocidad_oblique_x(dataFrame)