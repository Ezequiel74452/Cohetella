import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from utilsCinematica import *

pio.renderers.default = 'browser'
HTML_VERTICAL_NAME = "graficos_vertical.html"
HTML_OBLIQUE_NAME = "graficos_oblicuo.html"
COLOR_POSICION = 'black'
COLOR_VELOCIDAD = 'blue'
COLOR_ACELERACION = 'red'
COLOR_FUNCION_POSICION = 'green'
COLOR_TIROV_POSICION = 'orange'
COLOR_FUNCION_VELOCIDAD = 'red'

def graficar_csv_matplot():
    # Leer el archivo CSV
    dataFrame = pd.read_csv('data.csv')
    
    #Gráficas antiguas
    # Creamos una figura con 3 filas y 1 columna
    fig, axs = plt.subplots(3, 1, figsize=(10, 10))
    # Graficamos la posición
    axs[0].plot(dataFrame['Tiempo (s)'], dataFrame['Posición Y (m)'])
    axs[0].set_title('Posición de la botella en el tiempo')
    axs[0].set_ylabel('Posición (m)')
    axs[0].grid(True)
    # Graficamos la velocidad
    axs[1].plot(dataFrame['Tiempo (s)'], dataFrame['Velocidad (m/s)'], color='green', marker='.')
    axs[1].set_title('Velocidad de la botella en el tiempo')
    axs[1].set_ylabel('Velocidad (m/s)')
    axs[1].grid(True)
    # Graficamos la aceleración
    axs[2].plot(dataFrame['Tiempo (s)'], dataFrame['Aceleración (m/s^2)'], color='orange', marker='.')
    axs[2].set_title('Aceleración de la botella en el tiempo')
    axs[2].set_ylabel('Aceleración (m/s^2)')
    axs[2].set_xlabel('Tiempo (s)')
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()

def graficar_csv_plotly(path):
  dataFrame = pd.read_csv(path)
  return graficar_plotly(dataFrame)

def graficar_plotly(dataFrame):
    velocidad_ajustada, tiempo = ajustar_velocidad(dataFrame)
    
    # Crear una figura con subplots
    fig = make_subplots(rows=3, cols=1, 
                        vertical_spacing=0.1, 
                        subplot_titles=("Posición en el tiempo", "Velocidad en el tiempo", "Aceleración en el tiempo"))

    # Graficar la posición
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Posición Y (m)'],
        mode='lines',
        name='Posición (m)',
        line=dict(color=COLOR_POSICION)
    ), row=1, col=1)

    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Velocidad (m/s)'],
        mode='lines',
        name='Velocidad (m/s)',
        line=dict(color=COLOR_VELOCIDAD)
    ), row=2, col=1)
    
    #Graficar la funcion velocidad
    fig.add_trace(go.Scatter(
    x=tiempo,
    y=velocidad_ajustada,
    mode='lines',
    name='Velocidad ajustada (m/s)',
    line=dict(color=COLOR_FUNCION_VELOCIDAD, dash='dash')  # Línea punteada
    ), row=2, col=1)
    

    # Graficar la aceleración
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Aceleración (m/s^2)'],
        mode='lines',
        name='Aceleración (m/s^2)',
        line=dict(color=COLOR_ACELERACION)
    ), row=3, col=1)

    # Actualizar el diseño de la figura
    fig.update_layout(
        height=1200, # altura del gráfico
        title='Datos de la botella en el tiempo',
        legend_title='Tipo de Datos'
    )
    fig.update_xaxes(showgrid=True, gridcolor='LightGray')
    fig.update_xaxes(title_text="Tiempo (s)")
    fig.update_yaxes(title_text="Posición (m)", row=1, col=1)
    fig.update_yaxes(title_text="Velocidad (m/s)", row=2, col=1)
    fig.update_yaxes(title_text="Aceleración (m/s^2)", row=3, col=1)
    fig.update_yaxes(showgrid=True, gridcolor='LightGray')

    # Mostrar la figura en un solo archivo HTML
    fig.write_html(HTML_VERTICAL_NAME)
    return HTML_VERTICAL_NAME

def graficar_oblique_csv_plotly(path):
  dataFrame = pd.read_csv(path)
  return oblique_graph(dataFrame)

def oblique_graph(df):
    # Crear una figura con subplots para la posición

    fig = make_subplots(rows=3, cols=1, 
                        vertical_spacing=0.1, 
                        subplot_titles=("Posición x en el tiempo", "Posición y en el tiempo", "Trayectoria"))
    
    fig.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Posición X (m)'],
        mode='lines',
        name='Posición x (m)',
        line=dict(color=COLOR_POSICION)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Posición Y (m)'],
        mode='lines',
        name='Posición y (m)',
        line=dict(color=COLOR_POSICION)
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df['Posición X (m)'],
        y=df['Posición Y (m)'],
        mode='lines',
        name='Trayectoria',
        line=dict(color=COLOR_POSICION)
    ), row=3, col=1)
    
    fig.update_layout(
        height=1200, # altura del gráfico
        title='Trayectoria de la botella',
        legend_title='Tipo de datos'
    )
    
    fig.update_xaxes(showgrid=True, gridcolor='LightGray')
    fig.update_xaxes(title_text="Tiempo (s)", row=1, col=1)
    fig.update_xaxes(title_text="Tiempo (s)", row=2, col=1)
    fig.update_xaxes(title_text="Posición X (m)", row=3, col=1)
    
    fig.update_yaxes(title_text="Posición X (m)", row=1, col=1)
    fig.update_yaxes(title_text="Posición Y (m)", row=2, col=1)
    fig.update_yaxes(title_text="Posición Y (m)", row=3, col=1)
    
    fig.update_yaxes(showgrid=True, gridcolor='LightGray')
    
    #Crear una figura con subplots para la velocidad
    figVel = make_subplots(rows=2, cols=1,
                            vertical_spacing=0.1,
                            subplot_titles=("Velocidad x en el tiempo", "Velocidad y en el tiempo"))
    
    figVel.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Velocidad X (m/s)'],
        mode='lines',
        name='Velocidad x (m/s)',
        line=dict(color=COLOR_VELOCIDAD)
    ), row=1, col=1)
    
    figVel.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Velocidad Y (m/s)'],
        mode='lines',
        name='Velocidad y (m/s)',
        line=dict(color=COLOR_VELOCIDAD)
    ), row=2, col=1)
    
    figVel.update_layout(
        height=1200, # altura del gráfico
        title='Velocidad de la botella',
        legend_title='Tipo de datos'
    )
    
    figVel.update_xaxes(showgrid=True, gridcolor='LightGray')
    figVel.update_xaxes(title_text='Tiempo (s)')
    
    figVel.update_yaxes(showgrid=True, gridcolor='LightGray')
    figVel.update_yaxes(title_text='Velocidad en X (m/s)', row=1, col=1)
    figVel.update_yaxes(title_text='Velocidad en Y (m/s)', row=2, col=1)
    
    #Crear una figura con subplots para la aceleración
    figAcc = make_subplots(rows=2, cols=1,
                            vertical_spacing=0.1,
                            subplot_titles=("Aceleración x en el tiempo", "Aceleración y en el tiempo"))
    
    figAcc.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Aceleración X (m/s^2)'],
        mode='lines',
        name='Aceleración x (m/s^2)',
        line=dict(color=COLOR_ACELERACION)
    ), row=1, col=1)
    
    figAcc.add_trace(go.Scatter(
        x=df['Tiempo (s)'],
        y=df['Aceleración Y (m/s^2)'],
        mode='lines',
        name='Aceleración y (m/s^2)',
        line=dict(color=COLOR_ACELERACION)
    ), row=2, col=1)
    
    figAcc.update_layout(
        height=1200, # altura del gráfico
        title='Aceleración de la botella',
        legend_title='Tipo de datos'
    )
    figAcc.update_xaxes(showgrid=True, gridcolor='LightGray')
    figAcc.update_xaxes(title_text="Tiempo (s)")
    
    figAcc.update_yaxes(showgrid=True, gridcolor='LightGray')
    figAcc.update_yaxes(title_text="Aceleración X (m/s^2)", row=1, col=1)
    figAcc.update_yaxes(title_text="Aceleración Y (m/s^2)", row=2, col=1)
    
    with open(HTML_OBLIQUE_NAME, "w", encoding="utf-8") as f:
        # Guardar la primera figura con Plotly JS
        f.write(pio.to_html(fig, full_html=True))
        # Guardar las siguientes sin incluir Plotly JS nuevamente
        f.write(pio.to_html(figVel, full_html=False, include_plotlyjs=False))
        f.write(pio.to_html(figAcc, full_html=False, include_plotlyjs=False))
    
    return HTML_OBLIQUE_NAME

   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
