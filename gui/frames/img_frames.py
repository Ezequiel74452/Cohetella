import customtkinter as ctk
from abc import ABC
from gui.constants import *
from gui.img_output import ImageFrameOutput
from gui.options.options_gui import GUIVertical, GUIOblique
from PIL import Image, ImageTk

class ImageFrame(ctk.CTkFrame, ABC):
	def __init__(self, parent, img_path, restore_func, clear_func):
		super().__init__(parent, fg_color=DARKER_GRAY, corner_radius=30)

		self.img_path = img_path
		self.restore = restore_func
		self.clear = clear_func
		self.gui = None

		self.rowconfigure(0, weight=0)
		self.rowconfigure(1, weight=1)
		self.columnconfigure(0, weight=1)

		self.open_img()

	def open_img(self):
		if self.img_path != "":
			self.original_img = Image.open(self.img_path)
			self.img = self.original_img
			self.img_ratio = self.img.size[0] / self.img.size[1]
			self.img_tk = ImageTk.PhotoImage(self.img)
			self.img_output = ImageFrameOutput(self, self.resize_img, self.options_gui)

	def resize_img(self, event):
		self.canvas_h = event.height
		self.canvas_w = event.width
		canvas_ratio = self.canvas_w / self.canvas_h
		if canvas_ratio > self.img_ratio:
			self.img_h = self.canvas_h
			self.img_w = self.img_ratio * self.img_h
		else:
			self.img_w = self.canvas_w
			self.img_h = self.img_w / self.img_ratio
		self.place_img()

	def place_img(self):
		self.img_tk = ImageTk.PhotoImage(self.img.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w / 2, self.canvas_h / 2, image=self.img_tk)
	
	def options_gui(self, _):
		self.clear(self.gui)

class ImageFrameVertical(ImageFrame):
	def __init__(self, parent, img_path, restore_func, clear_func):
		super().__init__(parent, img_path, restore_func, clear_func)

		self.grid(row=0, column=1, columnspan=1, sticky="news", padx=40, pady=40)

		self.label_top = ctk.CTkLabel(self, text= "Tiro vertical",
												font= ctk.CTkFont(family= "Roboto", size= 40, weight= "bold"),
												text_color= LIGHT_GRAY, fg_color= DARKER_GRAY, bg_color= DARKER_GRAY)
		self.label_top.grid(row=0, column=0, padx=10, pady=(10, 0))
		self.gui = GUIVertical(parent, self.restore)

class ImageFrameOblique(ImageFrame):
	def __init__(self, parent, img_path, restore_func, clear_func):
		super().__init__(parent, img_path, restore_func, clear_func)

		self.grid(row=0, column=0, columnspan=1, sticky="news", padx=40, pady=40)

		self.label_top = ctk.CTkLabel(self, text= "Tiro oblicuo",
												font= ctk.CTkFont(family= "Roboto", size= 40, weight= "bold"),
												text_color= LIGHT_GRAY, fg_color= DARKER_GRAY, bg_color= DARKER_GRAY)
		self.label_top.grid(row=0, column=0, padx=10, pady=(10, 0))
		self.gui = GUIOblique(parent, self.restore)