import customtkinter as ctk
from constants import *

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color= DARK_GRAY)
        self.pack(fill= "x", pady=4, ipady= 8)

class OrigenPanel(Panel):
	def __init__(self, parent, func, X, Y, text):
		super().__init__(parent)
		self.func = func
		self.X = X
		self.Y = Y
		sel_origen_btn = ctk.CTkButton(self, text= f"Seleccionar {text}", command= self.func)
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