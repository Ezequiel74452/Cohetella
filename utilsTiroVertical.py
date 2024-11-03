def position_tiro_vertical(t, y0, v0):
    return y0 + v0 * t - 0.5 * 9.81 * t**2

def velocity_tiro_vertical(t, v0):
    return v0 - 9.81 * t