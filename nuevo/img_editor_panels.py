import customtkinter as ctk
from constants import *
from tkinter import filedialog

class Panel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color= DARK_GRAY)
        self.pack(fill= "x", pady=4, ipady= 8)

class SliderPanel(Panel):
    def __init__(self, parent, text, data_var, min_val, max_val):
        super().__init__(parent)
        self.columnconfigure((0, 1), weight= 1, uniform= "a")
        self.rowconfigure((0, 1), weight= 1, uniform= "a")
        self.data_var = data_var
        self.data_var.trace_add("write", self.update_text)
        
        ctk.CTkLabel(self, text= text).grid(column= 0, row= 0, sticky= "w", padx= 10)
        self.num_lbl = ctk.CTkLabel(self, text = data_var.get())
        self.num_lbl.grid(column= 1, row= 0, sticky= "e", padx= 10)
        slider = ctk.CTkSlider(self, fg_color= SLIDER_BG, variable= self.data_var, from_= min_val, to= max_val)
        slider.grid(column= 0, row= 1, columnspan= 2, sticky= "ew", padx= 10, pady= 5)
    
    def update_text(self, *args):
        self.num_lbl.configure(text= str(round(self.data_var.get(), 2)))

class SettingPanel(Panel):
	def __init__(self, parent, name_str, file_str, text):
		super().__init__(parent)
		self.columnconfigure(0, weight= 1, uniform= "a")
		self.rowconfigure((0, 1, 2), weight= 1, uniform= "a")

		self.name_str = name_str
		self.name_str.trace_add("write", self.update_name)
		self.file_str = file_str
		
		ctk.CTkLabel(self, text= text).grid(column= 0, row= 0, sticky= "w", padx= 10)
		entry = ctk.CTkEntry(self, textvariable= self.name_str, placeholder_text= "Unnamed")
		entry.grid(column= 0, row= 1, sticky= "ew", padx= 10, pady= 5)
		
		self.output = ctk.CTkLabel(self, text= "")
		self.output.grid(column= 0, row= 2, sticky= "ew", padx= 10, pady= 5)
	
	def update_name(self, *args):
		if self.name_str.get():
			self.output.configure(text= self.name_str.get()+" px")
		else:
			self.output.configure(text= "")

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