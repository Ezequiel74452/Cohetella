import customtkinter as ctk
from csv_widgets import CSVVerticalInput, CSVObliqueInput
from video_widgets import VideoObliqueInput, VideoVerticalInput
from abc import ABC
from close_btn import CloseBtn
from constants import *

class GUI(ctk.CTkFrame, ABC):
	def __init__(self, parent, restore):
		super().__init__(parent, fg_color= "transparent")
		
		#self.grid(column=0, row=0, columnspan=2, sticky="news", padx=20, pady=20)

		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1, uniform="a")
		self.columnconfigure(1, weight= 1, uniform="a")
		self.restore = restore
		self.close_btn = CloseBtn(parent= self, func= self.close_btn_func)
	
	def close_btn_func(self):
		self.grid_forget()
		self.restore()

class GUIVertical(GUI):
	def __init__(self, parent, restore):
		super().__init__(parent, restore)
		self.vid_input = VideoVerticalInput(self)
		self.csv_input = CSVVerticalInput(self)

class GUIOblique(GUI):
	def __init__(self, parent, restore):
		super().__init__(parent, restore)
		self.vid_input = VideoObliqueInput(self)
		self.csv_input = CSVObliqueInput(self)