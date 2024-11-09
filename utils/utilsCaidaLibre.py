def position_caida_libre(t, y0):
    return y0 + 0.5 * -9.81 * t**2

def velocity_caida_libre(t):
    return -9.81 * t