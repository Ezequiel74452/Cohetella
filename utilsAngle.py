import math

def calcular_angulo(X0, Y0, X1, Y1):
	# Calcular la pendiente
	if X1 == X0:  # Para evitar división por cero
		return 90.0  # La línea es vertical
	m = (Y1 - Y0) / (X1 - X0)
	
	# Calcular el ángulo en radianes
	theta_rad = math.atan(m)
	
	# Convertir a grados
	theta_deg = math.degrees(theta_rad)
	
	return round(theta_deg, 2)