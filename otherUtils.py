import pandas as pd

def alturaMaximaInicio(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[0]

def alturaMaximaFin(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[-1]

def puntoMedioAlturaMaxima(df: pd.DataFrame):
    # Obtener la primera y última fila donde se alcanza la altura máxima
    inicio = alturaMaximaInicio(df)
    fin = alturaMaximaFin(df)
    
    # Obtener los índices de estas filas
    indice_inicio = df.index[df['Posición Y (m)'] == inicio['Posición Y (m)']][0]
    indice_fin = df.index[df['Posición Y (m)'] == fin['Posición Y (m)']][-1]
    
    # Calcular el índice del punto medio
    indice_medio = (indice_inicio + indice_fin) // 2
    
    # Devolver la fila correspondiente al índice medio
    return df.iloc[indice_medio]

def velocidadMaximaInicial(df: pd.DataFrame):
	vel_max_incial = df['Velocidad (m/s)'].max()
	return df[df['Velocidad (m/s)'] == vel_max_incial].iloc[-1]

