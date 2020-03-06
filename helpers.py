import numpy as np

def cm_to_pixels (cm, ppcm):
    return round(cm / ppcm)


#returns [x,y]
def rotate_on_point (px, py, ox, oy, angle):
    angle = np.deg2rad(angle)
    return [np.cos(angle) * (px-ox) - np.sin(angle) * (py-oy) + ox,
            np.sin(angle) * (px-ox) + np.cos(angle) * (py-oy) + oy]

def rotate_on_point_rounded (px, py, ox, oy, angle):
    angle = np.deg2rad(angle)
    return [np.cos(angle) * (px-ox) - np.sin(angle) * (py-oy) + ox,
            np.sin(angle) * (px-ox) + np.cos(angle) * (py-oy) + oy]
