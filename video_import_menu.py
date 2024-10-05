import customtkinter as ctk
from abc import ABC, abstractmethod
from track_frame_tab import TrackFrameVertical, TrackFrameOblique
from angle_frame_tab import AngleFrame

class Menu(ctk.CTkTabview, ABC):
	def __init__(self, parent, enable_o, enable_i, enable_s, pasar_frame, path, change_func):
		super().__init__(parent, command= change_func)
		self.grid(column= 0, row= 0, sticky= "news")
		self.enable_o = enable_o
		self.enable_i = enable_i
		self.enable_s = enable_s
		self.pasar_frame = pasar_frame
		self.path = path
	
	@abstractmethod
	def create_tab(self):
		pass


class MenuVertical(Menu):
	def __init__(self, parent, enable_o, enable_i, enable_s, pasar_frame, path, change_func):
		super().__init__(parent, enable_o, enable_i, enable_s, pasar_frame, path, change_func)
		self.add("Tracker")
		self.add("Ángulos")
		self.create_tab()
	
	def create_tab(self):
		self.track_frame = TrackFrameVertical(self.tab("Tracker"), self.enable_o, self.path)
		self.angle_frame = AngleFrame(self.tab("Ángulos"), self.enable_i, self.enable_s, self.pasar_frame, self.path)

class MenuOblique(Menu):
	def __init__(self, parent, enable_o, enable_i, enable_s, pasar_frame, path, change_func):
		super().__init__(parent, enable_o, enable_i, enable_s, pasar_frame, path, change_func)
		self.add("Tracker")
		self.add("Ángulos")
		self.create_tab()
	
	def create_tab(self):
		self.track_frame = TrackFrameOblique(self.tab("Tracker"), self.enable_o, self.path)
		self.angle_frame = AngleFrame(self.tab("Ángulos"), self.enable_i, self.enable_s, self.pasar_frame, self.path)