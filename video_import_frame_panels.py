import customtkinter as ctk
from constants import *

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color= DARK_GRAY)
        self.pack(fill= "x", pady=4, ipady= 8)

class OrigenPanel(Panel):
	def __init__(self, parent, func, X, Y):
		super().__init__(parent)
		self.func = func
		self.X = X
		self.Y = Y
		sel_origen_btn = ctk.CTkButton(self, text= "Seleccionar origen", command= self.func)
		sel_origen_btn.pack(pady= 5)
		ctk.CTkLabel(self, text= "X:").pack()
		self.entry_x = ctk.CTkEntry(self, state= "readonly", textvariable= self.X)
		self.entry_x.pack(expand= True, fill= "both", padx= 5, pady= 5)
		ctk.CTkLabel(self, text= "Y:").pack()
		self.entry_y = ctk.CTkEntry(self, state= "readonly", textvariable= self.Y)
		self.entry_y.pack(expand= True, fill= "both", padx= 5, pady= 5)
	
	def updateX(self, value):
		self.X.set(value)

	def updateY(self, value):
		self.Y.set(value)

class FPSPanel(Panel):
	def __init__(self, parent, FPS):
		super().__init__(parent)

		self.fps_value = FPS
		self.fps_value.trace_add("write", self.update_name)

		ctk.CTkLabel(self, text= "FPS:").pack()
		entry = ctk.CTkEntry(self, textvariable= self.fps_value, placeholder_text= "Unnamed")
		entry.pack(fill= "x", padx= 20, pady= 5)
		self.alert_lbl = ctk.CTkLabel(self, text = "", text_color=ERROR_RED, font= ctk.CTkFont(family= "Roboto", size= 16, weight= "bold"),)
		self.alert_lbl.pack()

	def update_name(self, *args):
		if (not self.fps_value.get().isdigit()) and (self.fps_value.get()):
			self.alert_lbl.configure(text= "FPS inválidos.")
		else:
			self.alert_lbl.configure(text= "")