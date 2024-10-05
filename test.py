import numpy as np
import os
import pandas as pd
import plotly.graph_objects as go
import webbrowser
from scipy.optimize import curve_fit
from sympy import *
from utilsGraficas import oblique_graph, graficar_oblique_csv_plotly

CSV_PATH = "oblicuo120fps.csv"

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
	principal_vertical()