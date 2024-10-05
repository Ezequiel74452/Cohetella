import customtkinter as ctk
from csv_widgets import CSVVerticalInput, CSVObliqueInput
from video_widgets import VideoObliqueInput, VideoVerticalInput
from abc import ABC
from close_btn import CloseBtn
from constants import *

class GUI(ctk.CTkFrame, ABC):
	def __init__(self, parent, restore):
		super().__init__(parent, fg_color= "transparent")

		self.rowconfigure(0, weight= 1)
		self.columnconfigure((0,1), weight= 1, uniform="a")
		self.restore = restore
		self.close_btn = CloseBtn(parent= self, func= self.close_btn_func)
		self.vid_input = None
		self.csv_input = None
	
	def close_btn_func(self):
		self.grid_forget()
		self.event_generate('<<RestoreMainScreen>>', when='tail')
	
	def restore_screen(self):
		self.vid_input.grid(column= 0, row= 0, columnspan= 1, sticky= "news", padx= 40, pady= 40)
		self.csv_input.grid(column= 1, row= 0, columnspan= 1, sticky= "news", padx= 40, pady= 40)
		self.close_btn.place(relx= 0.995, rely= 0.005, anchor= "ne")
	
	def clear_screen_and_place(self, frame):
		self.vid_input.grid_forget()
		self.csv_input.grid_forget()
		self.close_btn.place_forget()
		frame.grid(column= 0, row= 0, columnspan= 2, sticky= "news")

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