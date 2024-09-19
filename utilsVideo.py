import cv2

PX_TO_CM = 0.64286
PX_TO_CM_OBLICUO = 0.9047

def rescaleFrame(frame, scale=0.75):
  width = frame.shape[1] * scale
  height = frame.shape[0] * scale
  dimensions = (int(width), int(height))
  return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

def fromPixelsToMeters(x):
  return x * PX_TO_CM / 100

def fromPixelsToMetersOblicuo(x):
  return x * PX_TO_CM_OBLICUO / 100