import customtkinter as ctk
import cv2
from abc import ABC, abstractmethod
from close_btn import CloseBtn
from img_output import ImageFrameOutput
from PIL import Image, ImageTk, ImageDraw
from video_import_menu import MenuOblique, MenuVertical

class Container(ctk.CTkFrame, ABC):
	def __init__(self, parent, path):
		super().__init__(parent)
		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1, uniform= "a")
		self.columnconfigure(1, weight= 3, uniform= "a")

		self.parent = parent
		self.path = path
		self.selection_enabled = False
		self.canvas_w = 0
		self.canvas_h = 0
		self.img_w = 0
		self.img_h = 0
		self.menu = None
		
		self.read_first_frame()

	def read_first_frame(self):
		cap = cv2.VideoCapture(self.path)
		_, frame = cap.read()
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.original_img = Image.fromarray(frame_rgb)
		self.img = self.original_img
		self.img_ratio = self.img.size[0]/self.img.size[1]
		self.img_tk = ImageTk.PhotoImage(self.img)
		self.img_output = ImageFrameOutput(self, self.resize_img, self.select_pixel)
		self.img_output.grid(column= 1, row= 0, columnspan=1, sticky= "news", padx= 15, pady= 15)
		self.close_btn = CloseBtn(parent= self, func= self.close_btn_func)
		self.create_menu()

	@abstractmethod
	def create_menu(self):
		pass

	def close_btn_func(self):
		self.grid_forget()
		self.parent.restore_screen()

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
		if not self.selection_enabled:
			return
		x = (event.x - self.img_offset_x) * (self.original_img.size[0] / self.img_tk.width())
		y = (event.y - self.img_offset_y) * (self.original_img.size[1] / self.img_tk.height())
		if 0 <= x < self.original_img.size[0] and 0 <= y < self.original_img.size[1]:
			self.menu.frame.origin.updateX(str(round(x)))
			self.menu.frame.origin.updateY(str(round(y)))
			self.draw_cross(x, y)
			self.disable_pixel_selection()

	def draw_cross(self, x, y):
		self.img_display = self.original_img.copy()
		draw = ImageDraw.Draw(self.img_display)
		cross_size = 20
		draw.line((x - cross_size, y, x + cross_size, y), fill="red", width=5)
		draw.line((x, y - cross_size, x, y + cross_size), fill="red", width=5)
		self.refresh_img()

	def refresh_img(self):
		self.img_tk = ImageTk.PhotoImage(self.img_display.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w/2, self.canvas_h/2, image= self.img_tk)

	def enable_pixel_selection(self):
		self.selection_enabled = True

	def disable_pixel_selection(self):
		self.selection_enabled = False

class ContainerVertical(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuVertical(self, self.enable_pixel_selection, self.path)

class ContainerOblique(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuOblique(self, self.enable_pixel_selection, self.path)