import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.io as pio
from plotly.subplots import make_subplots
from utils.utilsCinematica import *
from utils.utilsVideo import *

pio.renderers.default = 'browser'
HTML_VERTICAL_NAME = "graficos_vertical.html"
HTML_OBLIQUE_NAME = "graficos_oblicuo.html"
COLOR_POSICION = 'black'
COLOR_VELOCIDAD = 'blue'
COLOR_ACELERACION = 'red'

COLOR_FUNCION_POSICION_1 = 'orange'
COLOR_POSICION_CAIDA_LIBRE = 'green'
COLOR_FUNCION_POSICION_2 = 'red'
COLOR_POSICION_TIRO_VERTICAL = 'purple'

COLOR_FUNCION_VELOCIDAD_1 = 'red'
COLOR_FUNCION_VELOCIDAD_2 = 'orange'
COLOR_VELOCIDAD_CAIDA_LIBRE = 'green'
COLOR_VELOCIDAD_TIRO_VERTICAL = 'purple'

COLOR_MASA = 'blue'
COLOR_CANTIDAD_MOVIMIENTO = 'red'
COLOR_FUERZA = 'orange'

COLOR_ENERGIA_POTENCIAL = 'red'
COLOR_ENERGIA_CINETICA = 'blue'
COLOR_ENERGIA_MECANICA = 'green'

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
    
    alturaMaxProm = puntoMedioAlturaMaxima(dataFrame)
    velocidadMaxInicial = calcularVelocidadMaximaInicial(dataFrame)
    velocidadMaxFinal = calcularVelocidadMaximaFinal(dataFrame)
    
    #Comparación con caida libre desde el punto de altura máxima
    velocidad_ajustada_CL, tiempo_caida_libre, g_ajustado_CL, err_g_CL = ajustar_velocidad_CL(dataFrame, alturaMaxProm, velocidadMaxFinal)
    velocidad_caida_libre = calcular_velocidad_caida_libre(dataFrame, alturaMaxProm, velocidadMaxFinal)   
    posicion_ajustada_CL = ajustar_posicion_CL(dataFrame, alturaMaxProm, velocidadMaxFinal, g_ajustado_CL)
    posicion_caida_libre = calcular_posicion_caida_libre(dataFrame, alturaMaxProm, velocidadMaxFinal)
    
    #Comparación con tiro vertical desde el punto de máxima velocidad
    velocidad_ajustada_TV, tiempo_tiro_vertical, g_ajustado_TV, err_g_TV = ajustar_velocidad_TV(dataFrame, velocidadMaxInicial, velocidadMaxFinal)
    velocidad_tiro_vertical = calcular_velocidad_tiro_vertical(dataFrame, velocidadMaxInicial, velocidadMaxFinal)
    posicion_ajustada_TV = ajustar_posicion_TV(dataFrame, velocidadMaxInicial, velocidadMaxFinal, g_ajustado_TV)
    posicion_tiro_vertical = calcular_posicion_tiro_vertical(dataFrame, velocidadMaxInicial, velocidadMaxFinal)
    
    
    fig = make_subplots(rows=9, cols=1, 
                        vertical_spacing=0.05,
                        subplot_titles=("Posición en el tiempo", "Velocidad en el tiempo", "Aceleración en el tiempo", "Masa en el tiempo", "Cant. de Movimiento en el tiempo", "Fuerza en el tiempo", "Energía en el tiempo", "Energía en la altura", "Rozamiento con el aire"))
    
    graficar_posicion_vertical(fig, 
															dataFrame, 
															posicion_ajustada_CL, 
															posicion_caida_libre, 
															tiempo_caida_libre,
															posicion_ajustada_TV,
															posicion_tiro_vertical, 
															tiempo_tiro_vertical)
    
    graficar_velocidad_vertical(fig, 
                                dataFrame, 
                                velocidad_ajustada_CL, 
                                velocidad_caida_libre, 
                                tiempo_caida_libre,
                                velocidad_ajustada_TV,
                                velocidad_tiro_vertical, 
                                tiempo_tiro_vertical)
    
    graficar_aceleracion_vertical(fig, dataFrame)
    
    graficar_masa(fig, dataFrame)
    
    graficar_cantidad_movimiento(fig, dataFrame)
    
    graficar_fuerza(fig, dataFrame)
    
    graficar_energia(fig, dataFrame)
    
    graficar_energia_altura(fig, dataFrame)

    graficar_rozamiento_con_aire(fig, dataFrame)
    
    fig.update_layout(
        height=3600, # altura del gráfico
        title='Datos de la botella en el tiempo',
        legend_tracegroupgap=320
    )
    fig.update_layout(legend=dict(groupclick="toggleitem"))
    fig.update_xaxes(showgrid=True, gridcolor='LightGray')
    fig.update_xaxes(title_text="Tiempo (s)")
    fig.update_yaxes(title_text="Posición (m)", row=1, col=1)
    fig.update_yaxes(title_text="Velocidad (m/s)", row=2, col=1)
    fig.update_yaxes(title_text="Aceleración (m/s^2)", row=3, col=1)
    fig.update_yaxes(title_text="Masa (kg)", row=4, col=1)
    fig.update_yaxes(title_text="Cant. de Movimiento (kg*m/s)", row=5, col=1)
    fig.update_yaxes(title_text="Fuerza (N)", row=6, col=1)
    fig.update_yaxes(title_text="Energía (J)", row=7, col=1)
    fig.update_yaxes(title_text="Energía (J)", row=8, col=1)
    fig.update_xaxes(title_text="Posición Y (m)", row=8, col=1)
    fig.update_yaxes(title_text="Rozamiento viscoso", row=9, col=1)
    fig.update_xaxes(title_text="Velocidad (m/s)", row=9, col=1)
    fig.update_yaxes(showgrid=True, gridcolor='LightGray')
    
    # Guardar la figura como HTML, sin incluir el script Plotly (lo cargamos desde CDN)
    #fig.write_html(HTML_VERTICAL_NAME, include_plotlyjs='cdn')
    
    # Agregar contenido HTML adicional
    with open(HTML_VERTICAL_NAME, "w", encoding="utf-8") as f:
        f.write("<h1>Información obtenida en el trackeo del cohete</h1>")
        f.write(pio.to_html(fig, full_html=True))
        f.write("""
            <style>
                h1 {
                    color: #5D6D7E;
                    font-family: Arial, sans-serif;
                    margin-top: 40px;
                    align: center;
                    justify-content: center;
                    text-align: center;
                }
                h2 {
                    color: #2E86C1;
                    font-family: Arial, sans-serif;
                    margin-left: 40px;
                }
                p {
                    color: #5D6D7E;
                    font-size: 16px; 
                    font-family: 'Verdana', sans-serif; 
                    margin-left: 45px;
                }
            </style>
        """)
        f.write("<h2>Datos adicionales del lanzamiento</h2>")
        f.write("<p>La aceleración del lanzamiento calculada al realizar el ajuste de la velocidad en el tramo de caida libre es de: " 
                + str(round(g_ajustado_CL, 2)) + " +/- " + str(round(err_g_CL, 2)) + " m/s<sup>2</sup></p>")
        f.write("<p>La aceleración del lanzamiento calculada al realizar el ajuste de la velocidad en el tramo de tiro vertical es de: " 
                + str(round(g_ajustado_TV, 2)) + " +/- " + str(round(err_g_TV, 2)) + " m/s<sup>2</sup></p>")
    
    return HTML_VERTICAL_NAME

def graficar_posicion_vertical(fig, dataFrame, posicion_ajustada_CL, posicion_caida_libre, tiempo_caida_libre, posicion_ajustada_TV, posicion_tiro_vertical, tiempo_tiro_vertical):
    alturaMaxI = alturaMaximaInicio(dataFrame)
    alturaMaxF = alturaMaximaFin(dataFrame)
    alturaMaxM = (alturaMaxF['Tiempo (s)'] + alturaMaxI['Tiempo (s)'])/2
    
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Posición Y (m)'],
        mode='lines',
        name='Posición (m)',
        line=dict(color=COLOR_POSICION),
        showlegend=True,
        legendgroup='1',
        legendgrouptitle_text='Posiciones'
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_caida_libre,
        y=posicion_ajustada_CL,
        mode='lines',
        name='Posición ajustada (CL)',
        line=dict(color=COLOR_FUNCION_POSICION_1, dash='dash'),
        showlegend=True,
        legendgroup='1', 
        visible='legendonly'
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_caida_libre,
        y=posicion_caida_libre,
        mode='lines',
        name='Posición caida libre',
        line=dict(color=COLOR_POSICION_CAIDA_LIBRE, dash='dash'),
        showlegend=True,
        legendgroup='1',
        visible='legendonly' 
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_tiro_vertical,
        y=posicion_ajustada_TV,
        mode='lines',
        name='Posición ajustada (TV)',
        line=dict(color=COLOR_FUNCION_POSICION_2, dash='dash'),
        showlegend=True,
        legendgroup='1',
        visible='legendonly' 
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_tiro_vertical,
        y=posicion_tiro_vertical,
        mode='lines',
        name='Posición tiro vertical',
        line=dict(color=COLOR_POSICION_TIRO_VERTICAL, dash='dash'),
        showlegend=True,
        legendgroup='1',
        visible='legendonly' 
    ),row=1, col=1)
    
    print("ALTURA MAX M: ", alturaMaxM)
    fig.add_shape(type='line',
                  x0=alturaMaxM,
                  x1=alturaMaxM,
                  y0=dataFrame['Posición Y (m)'].min(),
                  y1=dataFrame['Posición Y (m)'].max(),
                  line=dict(color='red', dash='dash'))
    #fig.add_shape(type='line',
    #              x0=alturaMaxF['Tiempo (s)'],
    #              x1=alturaMaxF['Tiempo (s)'],
    #              y0=dataFrame['Posición Y (m)'].min(),
    #              y1=dataFrame['Posición Y (m)'].max(),
    #              line=dict(color='red', dash='dash'))
    
def graficar_velocidad_vertical(fig, dataFrame, velocidad_ajustada_CL, velocidad_caida_libre, tiempo_caida_libre, velocidad_ajustada_TV, velocidad_tiro_vertical, tiempo_tiro_vertical):
    
    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Velocidad (m/s)'],
        mode='lines',
        name='Velocidad (m/s)',
        line=dict(color=COLOR_VELOCIDAD),
        legendgroup='2',
        legendgrouptitle_text='Velocidades'
    ),row=2, col=1)
    
    #Graficar la velocidad ajustada en el intervalo de caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_caida_libre,
        y=velocidad_ajustada_CL,
        mode='lines',
        name='Velocidad ajustada (CL)',
        line=dict(color=COLOR_FUNCION_VELOCIDAD_1, dash='dash'),
        legendgroup='2',
        visible='legendonly' 
    ),row=2, col=1)
    
    #Graficar la velocidad esperada de una caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_caida_libre,
        y=velocidad_caida_libre,
        mode='lines',
        name='Velocidad de caida libre',
        line=dict(color=COLOR_VELOCIDAD_CAIDA_LIBRE, dash='dash'),
        legendgroup='2',
        visible='legendonly'  
    ),row=2, col=1)
    
    #Graficar la velocidad ajustada en el intervalo de tiro vertical
    fig.add_trace(go.Scatter(
        x=tiempo_tiro_vertical,
        y=velocidad_ajustada_TV,
        mode='lines',
        name='Velocidad ajustada (TV)',
        line=dict(color=COLOR_FUNCION_VELOCIDAD_2, dash='dash'),
        legendgroup='2',
        visible='legendonly' 
    ),row=2, col=1)
    
    #Graficar la velocidad esperada de un tiro vertical
    fig.add_trace(go.Scatter(
        x=tiempo_tiro_vertical,
        y=velocidad_tiro_vertical,
        mode='lines',
        name='Velocidad de tiro vertical',
        line=dict(color=COLOR_VELOCIDAD_TIRO_VERTICAL, dash='dash'),
        legendgroup='2',
        visible='legendonly'  
    ),row=2, col=1)
    


def graficar_aceleracion_vertical(fig, dataFrame):
    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Aceleración (m/s^2)'],
        mode='lines',
        name='Aceleración (m/s^2)',
        line=dict(color=COLOR_ACELERACION),
        legendgrouptitle_text='Aceleración',
        legendgroup='3'
    ),row=3, col=1)

def graficar_masa(fig, dataFrame):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Masa (kg)'],
        mode='lines',
        name='Masa (kg)',
        line=dict(color=COLOR_MASA),
        legendgrouptitle_text='Masa',
        legendgroup='4'
    ),row=4, col=1)
    
def graficar_cantidad_movimiento(fig, dataFrame):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Cantidad de Movimiento'],
        mode='lines',
        name='Cantidad de movimiento',
        line=dict(color=COLOR_CANTIDAD_MOVIMIENTO),
        legendgrouptitle_text='Movimiento',
        legendgroup='5'
    ),row=5, col=1)
    
def graficar_fuerza(fig, dataFrame):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Fuerza (N)'],
        mode='lines',
        name='Fuerza (N)',
        line=dict(color=COLOR_FUERZA),
        legendgrouptitle_text='Fuerza',
        legendgroup='6'
    ),row=6, col=1)

def graficar_energia(fig, dataFrame):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Energia Cinetica (J)'],
        mode='lines',
        name='Energía cinetica (J)',
        line=dict(color=COLOR_ENERGIA_CINETICA),
        legendgrouptitle_text='Energía',
        legendgroup='7'
    ),row=7, col=1)
    
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Energia Potencial (J)'],
        mode='lines',
        name='Energía potencial (J)',
        line=dict(color=COLOR_ENERGIA_POTENCIAL),
        legendgrouptitle_text='Energía',
        legendgroup='7'
    ),row=7, col=1)
    
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Energia Mecanica (J)'],
        mode='lines',
        name='Energía Mecánica (J)',
        line=dict(color=COLOR_ENERGIA_MECANICA),
        legendgrouptitle_text='Energía',
        legendgroup='7'
    ),row=7, col=1)
    
def graficar_energia_altura(fig, dataFrame):
    fig.add_trace(go.Scatter(
        x=dataFrame['Posición Y (m)'],
        y=dataFrame['Energia Cinetica (J)'],
        mode='lines',
        name='Energía cinetica (J)',
        line=dict(color=COLOR_ENERGIA_CINETICA),
        legendgrouptitle_text='Energía',
        legendgroup='8'
    ),row=8, col=1)
    
    fig.add_trace(go.Scatter(
        x=dataFrame['Posición Y (m)'],
        y=dataFrame['Energia Potencial (J)'],
        mode='lines',
        name='Energía potencial (J)',
        line=dict(color=COLOR_ENERGIA_POTENCIAL),
        legendgrouptitle_text='Energía',
        legendgroup='8'
    ),row=8, col=1)
    
    fig.add_trace(go.Scatter(
        x=dataFrame['Posición Y (m)'],
        y=dataFrame['Energia Mecanica (J)'],
        mode='lines',
        name='Energía Mecánica (J)',
        line=dict(color=COLOR_ENERGIA_MECANICA),
        legendgrouptitle_text='Energía',
        legendgroup='8'
    ),row=8, col=1)
    

def graficar_rozamiento_con_aire(fig, dataFrame):
	dataFrame_filtrado = dataFrame.iloc[::5]
	fig.add_trace(go.Scatter(
		x=dataFrame_filtrado['Velocidad (m/s)'],
		y=dataFrame_filtrado['Rozamiento viscoso (N)'],
		mode='lines+markers',
		name='Rozamiento viscoso (N)',
		line=dict(color='blue'),
		legendgrouptitle_text='Rozamiento',
		legendgroup='9'
	), row=9, col=1)
 



# --------------------- OBLICUO -----------------------------------------


def graficar_plotly_oblique(dataFrame):
	
	# Comparación con tiro oblicuo desde el punto de máxima velocidad
	velocidad_ajustada_x, tiempo_x, g_ajustado_x, err_g_x = ajustar_velocidad_oblique_x(dataFrame)
	velocidad_x = calcular_velocidad_oblique_x(dataFrame)
	velocidad_ajustada_y, tiempo_y, g_ajustado_y, err_g_y = ajustar_velocidad_oblique_y(dataFrame)
	velocidad_y = calcular_velocidad_oblique_y(dataFrame)

	posicion_ajustada_x = ajustar_posicion_oblique_x(dataFrame, g_ajustado_x)
	posicion_x = calcular_posicion_oblique_x(dataFrame)
	posicion_ajustada_y = ajustar_posicion_oblique_y(dataFrame, g_ajustado_y)
	posicion_y = calcular_posicion_oblique_y(dataFrame)

	fig = make_subplots(rows=6, cols=1, 
											vertical_spacing=0.05,
											subplot_titles=("Posición X en el tiempo",
																			"Posición Y en el tiempo",
																			"Velocidad X en el tiempo",
																			"Velocidad Y en el tiempo",
																			"Aceleración X en el tiempo",
																			"Aceleración Y en el tiempo"))
  
	graficar_posicion_oblique_x(fig, 
														dataFrame, 
														posicion_ajustada_x,
														posicion_x,
														tiempo_x)

	graficar_posicion_oblique_y(fig, 
														dataFrame, 
														posicion_ajustada_y, 
														posicion_y,
														tiempo_y)

	graficar_velocidad_oblique_x(fig, 
															dataFrame, 
															velocidad_ajustada_x, 
															velocidad_x, 
															tiempo_x)

	graficar_velocidad_oblique_y(fig, 
															dataFrame, 
															velocidad_ajustada_y, 
															velocidad_y, 
															tiempo_y)

	graficar_aceleracion_oblique(fig, dataFrame)

	fig.update_layout(
        height=2400, # altura del gráfico
        title='Datos de la botella en el tiempo',
        legend_tracegroupgap=260
	)
	fig.update_layout(legend=dict(groupclick="toggleitem"))
		
	fig.update_xaxes(showgrid=True, gridcolor='LightGray')
	fig.update_xaxes(title_text="Tiempo (s)")
	fig.update_yaxes(title_text="Posición X (m)", row=1, col=1)
	fig.update_yaxes(title_text="Posición Y (m)", row=2, col=1)
	fig.update_yaxes(title_text="Velocidad X (m/s)", row=3, col=1)
	fig.update_yaxes(title_text="Velocidad Y (m/s)", row=4, col=1)
	fig.update_yaxes(title_text="Aceleración X (m/s^2)", row=5, col=1)
	fig.update_yaxes(title_text="Aceleración Y (m/s^2)", row=6, col=1)
	fig.update_yaxes(showgrid=True, gridcolor='LightGray')
	
	# Guardar la figura como HTML, sin incluir el script Plotly (lo cargamos desde CDN)
	#fig.write_html(HTML_VERTICAL_NAME, include_plotlyjs='cdn')
	
	# Agregar contenido HTML adicional
	with open(HTML_OBLIQUE_NAME, "w", encoding="utf-8") as f:
			f.write("<h1>Información obtenida en el trackeo del cohete</h1>")
			f.write(pio.to_html(fig, full_html=True))
			f.write("""
					<style>
							h1 {
									color: #5D6D7E;
									font-family: Arial, sans-serif;
									margin-top: 40px;
									align: center;
									justify-content: center;
									text-align: center;
							}
							h2 {
									color: #2E86C1;
									font-family: Arial, sans-serif;
									margin-left: 40px;
							}
							p {
									color: #5D6D7E;
									font-size: 16px; 
									font-family: 'Verdana', sans-serif; 
									margin-left: 45px;
							}
					</style>
			""")
			f.write("<h2>Datos adicionales del lanzamiento</h2>")
			f.write("<p>La aceleración del lanzamiento calculada al realizar el ajuste de la velocidad en el eje X es de: " 
							+ str(round(g_ajustado_x, 2)) + " +/- " + str(round(err_g_x, 2)) + " m/s<sup>2</sup></p>")
			f.write("<p>La aceleración del lanzamiento calculada al realizar el ajuste de la velocidad en el eje Y es de: " 
							+ str(round(g_ajustado_y, 2)) + " +/- " + str(round(err_g_y, 2)) + " m/s<sup>2</sup></p>")
	
	return HTML_OBLIQUE_NAME


def graficar_posicion_oblique_y(fig, dataFrame, posicion_ajustada_y, posicion_y, tiempo_y):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Posición Y (m)'],
        mode='lines',
        name='Posición Y (m)',
        line=dict(color=COLOR_POSICION),
        showlegend=True,
        legendgroup='2',
        legendgrouptitle_text='Posiciones Y'
    ),row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_y,
        y=posicion_ajustada_y,
        mode='lines',
        name='Posición Y ajustada',
        line=dict(color=COLOR_FUNCION_POSICION_1, dash='dash'),
        showlegend=True,
        legendgroup='2',
				visible='legendonly' 
    ),row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_y,
        y=posicion_y,
        mode='lines',
        name='Posición Y teórica',
        line=dict(color=COLOR_POSICION_CAIDA_LIBRE, dash='dash'),
        showlegend=True,
        legendgroup='2',
        visible='legendonly' 
    ),row=2, col=1)

def graficar_posicion_oblique_x(fig, dataFrame, posicion_ajustada_x, posicion_x, tiempo_x):
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Posición X (m)'],
        mode='lines',
        name='Posición X (m)',
        line=dict(color=COLOR_POSICION),
        showlegend=True,
        legendgroup='1',
        legendgrouptitle_text='Posiciones X'
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_x,
        y=posicion_ajustada_x,
        mode='lines',
        name='Posición X ajustada',
        line=dict(color=COLOR_FUNCION_POSICION_1, dash='dash'),
        showlegend=True,
        legendgroup='1', 
        visible='legendonly'
    ),row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=tiempo_x,
        y=posicion_x,
        mode='lines',
        name='Posición X teórica',
        line=dict(color=COLOR_POSICION_CAIDA_LIBRE, dash='dash'),
        showlegend=True,
        legendgroup='1',
        visible='legendonly' 
    ),row=1, col=1)

def graficar_velocidad_oblique_x(fig, dataFrame, velocidad_ajustada_x, velocidad_x, tiempo_x):
    
    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Velocidad X (m/s)'],
        mode='lines',
        name='Velocidad X (m/s)',
        line=dict(color=COLOR_VELOCIDAD),
        legendgroup='3',
        legendgrouptitle_text='Velocidades X'
    ),row=3, col=1)

    #Graficar la velocidad ajustada en el intervalo de caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_x,
        y=velocidad_ajustada_x,
        mode='lines',
        name='Velocidad X ajustada',
        line=dict(color=COLOR_FUNCION_VELOCIDAD_1, dash='dash'),
        legendgroup='3',
        visible='legendonly' 
    ),row=3, col=1)
    
    #Graficar la velocidad esperada de una caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_x,
        y=velocidad_x,
        mode='lines',
        name='Velocidad X teórica',
        line=dict(color=COLOR_VELOCIDAD_CAIDA_LIBRE, dash='dash'),
        legendgroup='3',
        visible='legendonly'  
    ),row=3, col=1)
    
def graficar_velocidad_oblique_y(fig, dataFrame, velocidad_ajustada_y, velocidad_y, tiempo_y):
    
    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Velocidad Y (m/s)'],
        mode='lines',
        name='Velocidad Y (m/s)',
        line=dict(color=COLOR_VELOCIDAD),
        legendgroup='4',
        legendgrouptitle_text='Velocidades Y'
    ),row=4, col=1)
    
    #Graficar la velocidad ajustada en el intervalo de caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_y,
        y=velocidad_ajustada_y,
        mode='lines',
        name='Velocidad Y ajustada',
        line=dict(color=COLOR_FUNCION_VELOCIDAD_1, dash='dash'),
        legendgroup='4',
        visible='legendonly' 
    ),row=4, col=1)
    
    #Graficar la velocidad esperada de una caida libre
    fig.add_trace(go.Scatter(
        x=tiempo_y,
        y=velocidad_y,
        mode='lines',
        name='Velocidad Y teórica',
        line=dict(color=COLOR_VELOCIDAD_CAIDA_LIBRE, dash='dash'),
        legendgroup='4',
        visible='legendonly'  
    ),row=4, col=1)

def graficar_aceleracion_oblique(fig, dataFrame):
    # Graficar la velocidad
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Aceleración X (m/s^2)'],
        mode='lines',
        name='Aceleración X (m/s^2)',
        line=dict(color=COLOR_ACELERACION),
        legendgrouptitle_text='Aceleración X',
        legendgroup='5'
    ),row=5, col=1)
    fig.add_trace(go.Scatter(
        x=dataFrame['Tiempo (s)'],
        y=dataFrame['Aceleración Y (m/s^2)'],
        mode='lines',
        name='Aceleración y (m/s^2)',
        line=dict(color=COLOR_ACELERACION),
        legendgrouptitle_text='Aceleración Y',
        legendgroup='6'
    ), row=6, col=1)

def graficar_oblique_csv_plotly(path):
  dataFrame = pd.read_csv(path)
  return graficar_plotly_oblique(dataFrame)

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
    alturaMaxI = alturaMaximaInicio(df)
    alturaMaxF = alturaMaximaFin(df)
    fig.add_shape(type='line',
                  x0=alturaMaxI['Tiempo (s)'],
                  x1=alturaMaxI['Tiempo (s)'],
                  y0=df['Posición Y (m)'].min(),
                  y1=df['Posición Y (m)'].max(),
                  line=dict(color='red', dash='dash'),
									row=2, col=1)
    fig.add_shape(type='line',
                  x0=alturaMaxF['Tiempo (s)'],
                  x1=alturaMaxF['Tiempo (s)'],
                  y0=df['Posición Y (m)'].min(),
                  y1=df['Posición Y (m)'].max(),
                  line=dict(color='red', dash='dash'),
									row=2, col=1)
    
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