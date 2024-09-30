import cv2
import numpy as np
import matplotlib.pyplot as plt
import utilsVideo as uv
import pandas as pd
from sympy import *
from scipy.optimize import curve_fit
import plotly.graph_objects as go

def estetica(figura,x_name = '',y_name = '',title = '',w = 900,h = 450):
    figura.update_xaxes(showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True,title = x_name)#'cccccccccccccccc')
    figura.update_yaxes(showgrid=True,showline=True, linewidth=2, linecolor='black', mirror=True,title =y_name)


    figura.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        template="plotly_white",
        title=title,
        autosize=False,
        width=w,
        height=h,
        #yaxis = dict(range=[0,1]),
        #xaxis = dict(range=[0,1]),
        title_font = dict(size =20),
        legend=dict(orientation = 'v',
                    font = dict(size = 18),
                     yanchor="top",
                     y=0.95,
                     xanchor="right",
                     x=1,
                     bgcolor='rgba(255,255,255,0)',
                   )
    )

# Defino condiciones iniciales de posicion y velocidad
xo = 0
yo = 10
vox = 1
voy = 20.3

t = [0]
x = [xo]
y = [yo]
while y[-1] >= 0:
  t += [t[-1] + 0.03]
  x += [vox*t[-1] + xo]
  y += [-9.8*(t[-1]**2)/2 + voy*t[-1] + yo]

# invento un ruido que le sumo a las posiciones
mu_ruido = 0 #genero un ruido centrado en cero
sigma_x = 0.01 # La desviacion del ruido respecto del cero
sigma_y = 0.01 # La desviacion del ruido respecto del cero

ruido_x = np.random.normal(mu_ruido, sigma_x, len(t))
ruido_y = np.random.normal(mu_ruido, sigma_y, len(t))

#Sumo el ruido a X y a Y
x = x + ruido_x
y = y + ruido_y

fig = go.Figure()
fig.add_traces(go.Scatter(x = x, y = y, mode = 'markers'))
estetica(fig, title = 'Trayectoria (X en funcion de Y)', x_name = 'X', y_name = 'Y')
fig.show()

fig = go.Figure()
fig.add_traces(go.Scatter(x = t,y = y, mode='markers'))
estetica(fig,title='Y en funcion del tiempo')
fig.show()

df = pd.DataFrame()
df['t'] = t
df['x'] = x
df['y'] = y
df['vel_x'] = df.x.diff()/df.t.diff()
df['vel_y'] = df.y.diff()/df.t.diff()
df

fig = go.Figure()
fig.add_traces(go.Scatter(x = df.t, y = df.vel_y, mode = 'markers'))

def velocity(t,g,vo):
  return(g*t+vo)

df = df.dropna().copy() # Elimino las filas que tienen NaNs

popt, pcov = curve_fit(velocity, xdata = df.t, ydata = df.vel_y)
errs = np.sqrt(np.diag(pcov))
print(popt,errs)


