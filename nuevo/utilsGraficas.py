import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots

pio.renderers.default = 'browser'
HTML_NAME = "grafico_interactivo.html"
C_POS = 'black'
C_VEL = 'blue'
C_ACC = 'red'

def graficar_csv_matplot():
    # Leer el archivo CSV
    dataFrame = pd.read_csv('data.csv')
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
    # Leer el archivo CSV
    print("archivo leido")
    
    # Crear una figura con subplots
    fig = make_subplots(rows=4, cols=1, 
                        shared_xaxes=True, 
                        vertical_spacing=0.1, 
                        subplot_titles=("Posición en el tiempo", "Velocidad en el tiempo", "Aceleración en el tiempo"))

    # Graficar la posición
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Posición Y (m)'],
        mode='lines',
        name='Posición (m)',
        line=dict(color=C_POS)
    ), row=1, col=1)

    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Velocidad (m/s)'],
        mode='lines',
        #mode='markers+lines',
        name='Velocidad (m/s)',
        #marker=dict(color=c_vel),
        line=dict(color=C_VEL)
    ), row=2, col=1)

    # Graficar la aceleración
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Aceleración (m/s^2)'],
        mode='lines',
        #mode='markers+lines',
        name='Aceleración (m/s^2)',
        #marker=dict(color=c_acc),
        line=dict(color=C_ACC)
    ), row=3, col=1)

    # Actualizar el diseño de la figura
    fig.update_layout(
        height=1200, # altura del gráfico
        title='Datos de la botella en el tiempo',
        xaxis_title='Tiempo (s)',
        legend_title='Tipo de Datos'
    )
    fig.update_xaxes(showgrid=True, gridcolor='LightGray')
    fig.update_yaxes(showgrid=True, gridcolor='LightGray')

    # Mostrar la figura en un solo archivo HTML
    fig.write_html(HTML_NAME)
    return HTML_NAME

def oblique_graph(df):
	fig, axs = plt.subplots(1,3, figsize = (14,7))
	plt.title('Trayectoria de la botella')
	axs[0].plot(df['Tiempo (s)'], df['Posición X (m)'], marker='o')
	axs[0].set_xlabel('Tiempo (s)')
	axs[0].set_ylabel('X (m)')
	axs[1].plot(df['Tiempo (s)'], df['Posición Y (m)'], marker='o')
	axs[1].set_xlabel('Tiempo (s)')
	axs[1].set_ylabel('Y (m)')
	axs[2].plot(df['Posición X (m)'], df['Posición Y (m)'], marker='o')
	axs[2].set_xlabel('X (m)')
	axs[2].set_ylabel('Y (m)')
	plt.show()

	# Graficar la velocidad con posiciones suavizadas
	fig, axs = plt.subplots(1,2, figsize = (14,7))
	plt.title('Velocidad de la botella')
	axs[0].plot(df['Tiempo (s)'], df['Velocidad X (m/s)'], marker='o')
	axs[0].set_xlabel('Tiempo (s)')
	axs[0].set_ylabel('Vel_X (m/s)')
	axs[1].plot(df['Tiempo (s)'], df['Velocidad Y (m/s)'], marker='o')
	axs[1].set_xlabel('Tiempo (s)')
	axs[1].set_ylabel('Vel_Y (m/s)')
	plt.show()

	# Graficar la aceleración con posiciones suavizadas
	fig, axs = plt.subplots(1,2, figsize = (14,7))
	plt.title('Aceleración de la botella')
	axs[0].plot(df['Tiempo (s)'], df['Aceleración X (m/s^2)'], marker='o')
	axs[0].set_xlabel('Tiempo (s)')
	axs[0].set_ylabel('A_X (m/s^2)')
	axs[1].plot(df['Tiempo (s)'], df['Aceleración Y (m/s^2)'], marker='o')
	axs[1].set_xlabel('Tiempo (s)')
	axs[1].set_ylabel('A_Y (m/s^2)')
	plt.show()
