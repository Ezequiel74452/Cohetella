import cv2
import numpy as np
import pandas as pd
import utilsVideo as uv

def oblique_track(path, origen_y, origen_x, fps):
	cap = cv2.VideoCapture(path)
	VID_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	VID_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	PISO = VID_HEIGHT - int(origen_y)
	ORIGEN = int(origen_x)
	FPS = int(fps)

	datos = {'Tiempo (s)':np.array([]), 'Posición Y (px)':np.array([]), 'Posición X (px)':np.array([])}
	df = pd.DataFrame(data=datos)

	tracker = cv2.legacy.TrackerCSRT.create()

	ret, frame = cap.read()
	if not ret:
		print("No se pudo leer el video.")
		cap.release()
		cv2.destroyAllWindows()
		exit()

	bbox = cv2.selectROI(frame, False)
	if bbox != (0, 0, 0, 0):
		tracker.init(frame, bbox)

		frame_number = 0

		while True:
			ret, frame = cap.read()
			if not ret:
				break

			success, bbox = tracker.update(frame)
			if success:
				x, y, w, h = [int(v) for v in bbox]
				center_x = x + w // 2
				center_y = y + h // 2

				final_x = center_x-ORIGEN
				final_y = VID_HEIGHT-PISO-y + h // 2
				time_elapsed = frame_number / FPS
				
				datos_frame = {'Tiempo (s)':[time_elapsed], 'Posición Y (px)':[final_y], 'Posición X (px)':[final_x]}
				df_frame = pd.DataFrame(data=datos_frame)
				df = pd.concat([df, df_frame], ignore_index=True)

				cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
				cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

			frame_number += 1

			cv2.imshow('Tracking', frame)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

		cap.release()
		cv2.destroyAllWindows()

		df = uv.posicion_en_metros_oblicuo(df)
		df = uv.suavizar_df_oblicuo(df)
		df = uv.calcular_velocidad_oblicuo(df)
		df = uv.calcular_aceleracion_oblicuo(df)

		return df

	cap.release()
	cv2.destroyAllWindows()

	return None

def vertical_track(path, origen_y, origen_x, fps):
	videoCapturado = cv2.VideoCapture(path) 

	ret, primerFrame = videoCapturado.read()
	if not ret:
			print("No se pudo leer el video.")
			videoCapturado.release()
			cv2.destroyAllWindows()
			exit()

	VID_WIDTH = int(videoCapturado.get(cv2.CAP_PROP_FRAME_WIDTH))
	VID_HEIGHT = int(videoCapturado.get(cv2.CAP_PROP_FRAME_HEIGHT))
	PISO = VID_HEIGHT - int(origen_y)
	ORIGEN = int(origen_x)
	FPS = int(fps)

	dataFrame = pd.DataFrame(data= {'Tiempo (s)':np.array([]), 'Posición Y (px)':np.array([])})

	tracker = cv2.legacy.TrackerCSRT.create()
	frame_resized = uv.rescaleFrame(primerFrame, scale=.5)
	bbox = cv2.selectROI(frame_resized, False)
	if bbox != (0, 0, 0, 0):
		tracker.init(frame_resized, bbox)

		#comienza a procesar frame por frame:
		frame_nro = 0
		while True:
				#captura el proximo frame
				exito, frame_actual = videoCapturado.read()
				if not exito:
						break
				frame_resized = uv.rescaleFrame(frame_actual, scale=.5)

				# Actualizar el rastreador
				success, bbox = tracker.update(frame_resized)
				if success:
						x, y, w, h = [int(v) for v in bbox]
						center_x = x + w // 2
						center_y = y + h // 2

						# Guardar las posiciones de acuerdo a nuestro sistema de coordenadas
						final_y = VID_HEIGHT - PISO - (center_y * 2)

						# Calcular el tiempo correspondiente a este fotograma
						time_elapsed = frame_nro / FPS  # Tiempo en segundos

						datos_del_frame = {'Tiempo (s)':[time_elapsed], 'Posición Y (px)':[final_y]}

						dataFrameAuxiliar = pd.DataFrame(data=datos_del_frame)
						dataFrame = pd.concat([dataFrame, dataFrameAuxiliar], ignore_index=True)

						print(f"Y: {final_y}, Tiempo: {time_elapsed}")

						# Dibujar la caja y el centro
						cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
						cv2.circle(frame_resized, (center_x, center_y), 5, (0, 0, 255), -1)

				frame_nro += 1

				# Mostrar el fotograma
				cv2.imshow('Tracking', frame_resized)
				if cv2.waitKey(1) & 0xFF == ord('q'):
						break

		videoCapturado.release()
		cv2.destroyAllWindows()

		dataFrame = uv.posicion_en_metros_vertical(dataFrame)
		dataFrame = uv.suavizar_df_vertical(dataFrame)
		dataFrame = uv.calcular_velocidad_vertical(dataFrame)
		dataFrame = uv.calcular_aceleracion_vertical(dataFrame)
		dataFrame = uv.calcular_masa_vertical(dataFrame)
		dataFrame = uv.calcular_cantidad_movimiento(dataFrame)
		dataFrame = uv.calcular_fuerza(dataFrame)
		dataFrame = uv.calcular_energia_cinetica(dataFrame)
		dataFrame = uv.calcular_energia_potencial(dataFrame)
		dataFrame = uv.calcular_energia_mecanica(dataFrame)

		return dataFrame
	
	videoCapturado.release()
	cv2.destroyAllWindows()

	return None