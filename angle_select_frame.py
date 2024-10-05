import customtkinter as ctk
import cv2
import numpy as np
import pandas as pd
from img_output import ImageFrameOutput
from PIL import Image, ImageTk, ImageDraw
from utilsAngle import calcular_angulo
from succesful_track_frame import EndOfVideoFrame

class AngleSelect(ctk.CTkFrame):
	def __init__(self, parent, path):
		super().__init__(parent)

		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1)

		self.parent = parent
		self.path = path
		self.selection_enabled_i = False
		self.selection_enabled_s = False
		self.canvas_w = 0
		self.canvas_h = 0
		self.img_w = 0
		self.img_h = 0
		self.cross = [None, None]
		self.cap = cv2.VideoCapture(self.path)
		datos = {'Pos. inferior':np.array([]),
						'Pos. superior':np.array([]),
						'Frame':np.array([]),
						'Ángulo':np.array([])}
		self.df = pd.DataFrame(data=datos)
		self.num_frame = 0
		
		self.read_first_frame()

	def read_first_frame(self):
		self.num_frame += 1
		ret, frame = self.cap.read()
		if not ret:
			self.cap.release()
			cv2.destroyAllWindows()
			exit()
		self.read_frame(frame)
	
	def next_second(self):
		for _ in range(120):
			self.num_frame += 1
			ret, frame = self.cap.read()
			if not ret:
				self.cap.release()
				cv2.destroyAllWindows()
				root = self.winfo_toplevel()
				for widget in root.winfo_children():
					widget.destroy()
				EndOfVideoFrame(root, self.df)
				return
		self.read_frame(frame)

	def read_frame(self, frame):
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.original_img = Image.fromarray(frame_rgb)
		self.img = self.original_img
		self.img_ratio = self.img.size[0]/self.img.size[1]
		self.img_tk = ImageTk.PhotoImage(self.img)
		self.img_output = ImageFrameOutput(self, self.resize_img, self.select_pixel)
		self.img_output.grid(column= 0, row= 0, columnspan=1, sticky= "news")

	def resize_img(self, event):
		self.canvas_h = event.height
		self.canvas_w = event.width
		canvas_ratio = self.canvas_w / self.canvas_h
		if canvas_ratio > self.img_ratio:
			self.img_h = self.canvas_h
			self.img_offset_y = 0
			self.img_w = self.img_ratio * self.img_h
			self.img_offset_x = (self.canvas_w-self.img_w) / 2
		else:
			self.img_w = self.canvas_w
			self.img_offset_x = 0
			self.img_h = self.img_w / self.img_ratio
			self.img_offset_y = (self.canvas_h-self.img_h) / 2
		self.place_img()

	def place_img(self):
		self.img_tk = ImageTk.PhotoImage(self.img.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w/2, self.canvas_h/2, image= self.img_tk)

	def select_pixel(self, event):
		if self.selection_enabled_i:
			self.select_pixel_i(event)
		elif self.selection_enabled_s:
			self.select_pixel_s(event)

	def select_pixel_i(self, event):
		x = (event.x - self.img_offset_x) * (self.original_img.size[0] / self.img_tk.width())
		y = (event.y - self.img_offset_y) * (self.original_img.size[1] / self.img_tk.height())
		if 0 <= x < self.original_img.size[0] and 0 <= y < self.original_img.size[1]:
			self.parent.menu.angle_frame.updateX_i(str(round(x)))
			self.parent.menu.angle_frame.updateY_i(str(round(y)))
			self.draw_cross(x, y)
			self.disable_pixel_selection_i()
	
	def select_pixel_s(self, event):
		x = (event.x - self.img_offset_x) * (self.original_img.size[0] / self.img_tk.width())
		y = (event.y - self.img_offset_y) * (self.original_img.size[1] / self.img_tk.height())
		if 0 <= x < self.original_img.size[0] and 0 <= y < self.original_img.size[1]:
			self.parent.menu.angle_frame.updateX_s(str(round(x)))
			self.parent.menu.angle_frame.updateY_s(str(round(y)))
			self.draw_cross(x, y)
			self.disable_pixel_selection_s()

	def draw_cross(self, x0, y0):
		self.img_display = self.original_img.copy()
		if self.selection_enabled_i:
			self.cross[0] = (x0, y0)
			if self.cross[1] is not None:
				x1, y1 = self.cross[1]
				self.draw((x0, y0), (x1, y1))
			else:
				self.draw((x0, y0), None)
		else:
			self.cross[1] = (x0, y0)
			if self.cross[0] is not None:
				x, y = self.cross[0]
				self.draw((x, y), (x0, y0))
			else:
				self.draw(None, (x0, y0))
		self.refresh_img(self.img_display)

	def draw(self, xy0, xy1):
		draw = ImageDraw.Draw(self.img_display)
		cross_size = 20
		if xy0 is not None:
			x, y = xy0
			draw.line((x - cross_size, y, x + cross_size, y), fill="red", width=5)
			draw.line((x, y - cross_size, x, y + cross_size), fill="red", width=5)
		if xy1 is not None:
			x, y = xy1
			draw.line((x - cross_size, y, x + cross_size, y), fill="red", width=5)
			draw.line((x, y - cross_size, x, y + cross_size), fill="red", width=5)

	def refresh_img(self, img):
		self.img_tk = ImageTk.PhotoImage(img.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w/2, self.canvas_h/2, image= self.img_tk)

	def enable_pixel_selection_i(self):
		self.selection_enabled_i = True
		self.selection_enabled_s = False

	def disable_pixel_selection_i(self):
		self.selection_enabled_i = False

	def enable_pixel_selection_s(self):
		self.selection_enabled_s = True
		self.selection_enabled_i = False

	def disable_pixel_selection_s(self):
		self.selection_enabled_s = False

	def mostrar(self):
		self.grid(column= 1, row= 0, sticky= "news", padx= 15, pady= 15)

	def ocultar(self):
		self.grid_forget()
	
	def pasar_frame(self):
		if self.cross[0] is not None and self.cross[1] is not None:
			x_i, y_i = self.cross[0]
			x_i_final = round(x_i)
			rounded_y_i = round(y_i)
			y_i_final = self.original_img.height - rounded_y_i
			x_s, y_s = self.cross[1]
			x_s_final = round(x_s)
			rounded_y_s = round(y_s)
			y_s_final = self.original_img.height - rounded_y_s
			angulo = calcular_angulo(x_i_final, y_i_final, x_s_final, y_s_final)
		else:
			x_i_final = None
			y_i_final = None
			x_s_final = None
			y_s_final = None
			angulo = None
		datos_frame = {'Pos. inferior':[(x_i_final, y_i_final)],
									'Pos. superior':[(x_s_final, y_s_final)],
									'Frame':[self.num_frame],
									'Ángulo':[angulo]}
		df_frame = pd.DataFrame(data=datos_frame)
		self.df = pd.concat([self.df, df_frame], ignore_index=True)
		print(self.df)
		self.cross[0] = None
		self.cross[1] = None
		self.selection_enabled_i = False
		self.selection_enabled_s = False
		self.parent.menu.angle_frame.updateX_i(str(0))
		self.parent.menu.angle_frame.updateY_i(str(0))
		self.parent.menu.angle_frame.updateX_s(str(0))
		self.parent.menu.angle_frame.updateY_s(str(0))
		self.next_second()
