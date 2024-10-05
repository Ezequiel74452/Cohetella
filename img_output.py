import customtkinter as ctk
from constants import *

class ImageFrameOutput(ctk.CTkCanvas):
	def __init__(self, parent, func_config, func_options):
		super().__init__(parent, bg= BG_COLOR, bd= 0, highlightthickness= 0, relief= "ridge")
		self.func_config = func_config
		self.func_options = func_options
		self.grid(column= 0, row= 1, columnspan=1, sticky= "news", padx= 15, pady= 15)
		self.bind("<Configure>", self.func_config)
		self.bind("<Button-1>", self.func_options)