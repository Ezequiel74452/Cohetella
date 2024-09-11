import cv2

def rescaleFrame(frame, scale=0.75):
  width = frame.shape[1] * scale
  height = frame.shape[0] * scale
  dimensions = (int(width), int(height))
  return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)