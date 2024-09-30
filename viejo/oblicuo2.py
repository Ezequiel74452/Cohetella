import cv2
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import filedialog

class VideoTracker:
    def __init__(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.VID_WIDTH = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.VID_HEIGHT = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.PISO = self.VID_HEIGHT - 477
        self.ORIGEN = 268
        self.FPS = 240

        self.datos = {'Tiempo (s)': np.array([]), 'Posición Y (px)': np.array([]), 'Posición X (px)': np.array([])}
        self.df = pd.DataFrame(data=self.datos)

        self.tracker = cv2.legacy.TrackerCSRT.create()
        self.frame_number = 0

        # Iniciar GUI
        self.root = tk.Tk()
        self.root.title("Video Tracker")
        
        self.canvas = tk.Canvas(self.root, width=self.VID_WIDTH, height=self.VID_HEIGHT)
        self.canvas.pack()

        self.btn_select = tk.Button(self.root, text="Seleccionar Área", command=self.select_roi)
        self.btn_select.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def select_roi(self):
        ret, frame = self.cap.read()
        if not ret:
            print("No se pudo leer el video.")
            self.cap.release()
            self.root.destroy()
            return

        bbox = cv2.selectROI(frame, False)
        self.tracker.init(frame, bbox)
        self.track_video(frame)

    def track_video(self, initial_frame):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            success, bbox = self.tracker.update(frame)
            if success:
                x, y, w, h = [int(v) for v in bbox]
                center_x = x + w // 2
                center_y = y + h // 2

                # Guardar las posiciones
                final_x = center_x - self.ORIGEN
                final_y = self.VID_HEIGHT - self.PISO - y + h // 2
                time_elapsed = self.frame_number / self.FPS

                datos_frame = {'Tiempo (s)': [time_elapsed], 'Posición Y (px)': [final_y], 'Posición X (px)': [final_x]}
                df_frame = pd.DataFrame(data=datos_frame)
                self.df = pd.concat([self.df, df_frame], ignore_index=True)

                # Dibujar la caja y el centro
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)

            self.frame_number += 1

            # Mostrar el fotograma en el canvas
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(frame, (self.VID_WIDTH, self.VID_HEIGHT))
            img = np.array(img)
            img = tk.PhotoImage(image=tk.Image.fromarray(img))

            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
            self.canvas.update()
            self.root.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        self.root.destroy()

    def on_closing(self):
        self.cap.release()
        self.root.destroy()

# Selecciona el video
root = tk.Tk()
root.withdraw()  # Oculta la ventana principal
video_path = filedialog.askopenfilename(title="Seleccionar video", filetypes=[("Video Files", "*.MOV;*.mp4")])
if video_path:
    VideoTracker(video_path)