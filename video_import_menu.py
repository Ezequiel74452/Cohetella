import customtkinter as ctk
from abc import ABC, abstractmethod
from video_import_menu_frame import TrackFrameVertical, TrackFrameOblique

class Menu(ctk.CTkTabview, ABC):
	def __init__(self, parent, func, path):
		super().__init__(parent)
		self.grid(column= 0, row= 0, sticky= "news")
		self.func = func
		self.path = path
	
	@abstractmethod
	def create_tab(self):
		pass

class MenuVertical(Menu):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
		self.add("Menú")
		self.create_tab()
	
	def create_tab(self):
		self.frame = TrackFrameVertical(self.tab("Menú"), self.func, self.path)

class MenuOblique(Menu):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
		self.add("Menú")
		self.create_tab()
	
	def create_tab(self):
		self.frame = TrackFrameOblique(self.tab("Menú"), self.func, self.path)