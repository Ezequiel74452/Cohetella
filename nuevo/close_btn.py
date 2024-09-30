import customtkinter as ctk
from constants import *

class CloseBtn(ctk.CTkButton):
	def __init__(self, parent, func):
			super().__init__(parent, text= "X", text_color= WHITE, fg_color= "transparent", width= 30, height= 30, corner_radius= 0, hover_color= CLOSE_RED, command= func)
			self.place(relx= 0.995, rely= 0.005, anchor= "ne")
			self.lift()