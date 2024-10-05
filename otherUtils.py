import pandas as pd

def alturaMaximaInicio(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[0]

def alturaMaximaFin(df: pd.DataFrame):
	pos_max = df['Posición Y (m)'].max()
	return df[df['Posición Y (m)'] == pos_max].iloc[-1]