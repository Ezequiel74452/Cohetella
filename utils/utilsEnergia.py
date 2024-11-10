def calcular_energia_cinetica(df):
  df['Energia Cinetica (J)'] = 0.5 * df['Masa (kg)'] * df['Velocidad (m/s)']**2
  return df

def calcular_energia_potencial(df):
  df['Energia Potencial (J)'] = df['Masa (kg)'] * 9.81 * df['Posición Y (m)']
  return df

def calcular_energia_mecanica(df):
  df['Energia Mecanica (J)'] = df['Energia Cinetica (J)'] + df['Energia Potencial (J)']
  return df