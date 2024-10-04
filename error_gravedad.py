import pandas as pd
import numpy

def main():
    # Leer el archivo 
    path = "vertical.csv"
    dataFrame = pd.read_csv(path)
    t0_mruv = 0.7
    tf_mruv = 2
    PX_TO_CM = 0.64286
    sigma_nom = PX_TO_CM * 0.01

    # Filtrar el DataFrame según el rango de tiempo
    filtered_df = dataFrame.loc[(dataFrame['Tiempo (s)'] >= t0_mruv) & (dataFrame['Tiempo (s)'] <= tf_mruv)]

    #calculo la gravedad promedio para los puntos registrados
    g_medidos = filtered_df['Aceleración (m/s^2)'].tolist()
    g_prom = numpy.mean(g_medidos)
    print("aceleracion promedio: " + str(g_prom))

    #calculo el desvio estandar
    desv_est_g = numpy.std(g_medidos)
    print("desvio estadar de la acc: " + str(desv_est_g))

    #error:
    error = numpy.sqrt(desv_est_g**2 + sigma_nom**2)
    error = float('%.1g' % desv_est_g)
    print("g = [" + str(round(g_prom,2)) + " +/- " + str(error) + "]m/s2")
main()