def pos_oblique_x(t, x0, v0=0):
	return x0 + v0 * t

def pos_oblique_y(t, y0, v0=0):
	return y0 + v0 * t - 0.5 * 9.81 * t**2

def position_oblique_x(t, x0, g, v0=0):
		return x0 + v0 * t + 0.5 * g * t**2

def position_oblique_y(t, y0, g, v0=0):
		return y0 + v0 * t + 0.5 * g * t**2

def vel_oblique_x(t, v0):
	return v0 + 0*t

def vel_oblique_y(t, v0):
    return v0 -9.81 * t

"""def velocity_oblique_x(t, g, v0=0):
	return v0 + g * t"""

"""def velocity_oblique_y(t, g, v0=0):
	return v0 + g * t"""

def velocity_oblique_x(t, g):
	v0 = 6.64
	return v0 + g * t

def velocity_oblique_y(t, g):
	v0 = 7.1
	return v0 + g * t