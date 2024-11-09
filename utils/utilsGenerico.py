def position(t, y0, g, v0=0):
    return y0 + v0 * t + 0.5 * g * t**2

def velocity(t, g, v0=0):
    return v0 +g * t