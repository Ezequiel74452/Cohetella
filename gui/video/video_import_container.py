import customtkinter as ctk
from abc import ABC, abstractmethod
from gui.options.close_btn import CloseBtn
from gui.frames.origin_select_frame import OriginSelect
from gui.angles.angle_select_frame import AngleSelect
from gui.video.video_import_menu import MenuOblique, MenuVertical

class Container(ctk.CTkFrame, ABC):
	def __init__(self, parent, path):
		super().__init__(parent)
		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1, uniform= "a")
		self.columnconfigure(1, weight= 3, uniform= "a")

		self.parent = parent
		self.path = path
		self.origin_select_frame = OriginSelect(self, self.path)
		self.origin_select_frame.mostrar()
		self.angle_select_frame = AngleSelect(self, self.path)
		self.close_btn = CloseBtn(parent= self, func= self.close_btn_func)
		self.active = 0
		self.menu = None
		
		self.create_menu()

	def select(self):
		if self.active == 0:
			self.origin_select_frame.ocultar()
			self.angle_select_frame.mostrar()
			self.active = 1
		else:
			self.angle_select_frame.ocultar()
			self.origin_select_frame.mostrar()
			self.active = 0

	@abstractmethod
	def create_menu(self):
		pass

	def close_btn_func(self):
		self.grid_forget()
		self.parent.restore_screen()

class ContainerVertical(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuVertical(self,
														self.origin_select_frame.enable_pixel_selection,
														self.angle_select_frame.enable_pixel_selection_i,
														self.angle_select_frame.enable_pixel_selection_s,
														self.angle_select_frame.pasar_frame,
														self.path,
														self.select)

class ContainerOblique(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuOblique(self,
														self.origin_select_frame.enable_pixel_selection,
														self.angle_select_frame.enable_pixel_selection_i,
														self.angle_select_frame.enable_pixel_selection_s,
														self.angle_select_frame.pasar_frame,
														self.path,
														self.select)