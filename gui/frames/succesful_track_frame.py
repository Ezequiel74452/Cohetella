import webbrowser
import customtkinter as ctk
from abc import ABC, abstractmethod
from gui.constants import *
from tkinter import messagebox
import os
from utils.utilsGraficas import oblique_graph, graficar_plotly

class SuccesfulTrackFrame(ctk.CTkFrame, ABC):
	def __init__(self, parent, df):
		super().__init__(parent, fg_color= "transparent")
		self.grid(column= 0, row= 0, columnspan= 2, sticky= "news", padx= 10, pady= 10)
		self.df = df
		self.columnconfigure(0, weight= 1)
		self.rowconfigure(0, weight= 10)
		self.rowconfigure(1, weight= 1)

		lbl = ctk.CTkLabel(self, text= "El video se ha trackeado correctamente",
												font= ctk.CTkFont(family= "Robot", size= 40, weight= "bold"),
												text_color= LIGHT_GRAY, fg_color= "transparent", bg_color= "transparent",
												justify= "center")
		lbl.grid(row=0, column=0, padx= 10, sticky= "news")

		btns = ButtonFrame(self, self.graph, self.csv)
		btns.grid(row=1, column=0, padx= 10, sticky= "news")

	@abstractmethod
	def graph(self):
		pass

	def csv(self):
		dialog = ctk.CTkInputDialog(text="Ingrese el nombre del archivo", title="Guardar como csv")
		text = dialog.get_input()
		if text is not None:
			if not text.endswith(".csv"):
				text = f"{text}.csv"
			self.df.to_csv(text, index=False)
			messagebox.showinfo("Información", f"Se ha guardado el archivo como {text}")

class SuccesfulTrackFrameVertical(SuccesfulTrackFrame):
	def __init__(self, parent, df):
		super().__init__(parent, df)

	def graph(self):
		path_to_html = graficar_plotly(self.df)
		file_url = 'file://' + os.path.abspath(path_to_html).replace('\\', '/')
		webbrowser.open(file_url)

class SuccesfulTrackFrameOblique(SuccesfulTrackFrame):
	def __init__(self, parent, df):
		super().__init__(parent, df)

	def graph(self):
		path_to_html = oblique_graph(self.df)
		file_url = 'file://' + os.path.abspath(path_to_html).replace('\\', '/')
		webbrowser.open(file_url)
	

class ButtonFrame(ctk.CTkFrame):
	def __init__(self, parent, graph, save):
		super().__init__(parent, fg_color= "transparent")
		self.columnconfigure((0,1), weight= 1)
		self.rowconfigure(0, weight= 1)

		self.btn_graph = ctk.CTkButton(self, text="Graficar", command=graph)
		self.btn_graph.grid(row=0, column=0, sticky="nsew", padx= 10)
		self.btn_save = ctk.CTkButton(self, text="Guardar como .csv", command=save)
		self.btn_save.grid(row=0, column=1, sticky="nsew", padx= 10)

class EndOfVideoFrame(ctk.CTkFrame):
	def __init__(self, parent, df):
		super().__init__(parent, fg_color= "transparent")
		self.grid(column= 0, row= 0, columnspan= 2, sticky= "news", padx= 10, pady= 10)
		self.columnconfigure(0, weight= 1)
		self.rowconfigure(0, weight= 10)
		self.rowconfigure(1, weight= 1)
		self.df = df
		lbl = ctk.CTkLabel(self, text= "El video ha finalizado",
											font= ctk.CTkFont(family= "Robot", size= 40, weight= "bold"),
											text_color= LIGHT_GRAY, fg_color= "transparent", bg_color= "transparent",
											justify= "center")
		lbl.grid(row=0, column=0, padx= 10, sticky= "news")
		self.btn = ctk.CTkButton(self, text= "Guardar datos como .csv", command= self.csv)
		self.btn.grid(row=1, column=0, padx= 10, sticky= "news")
	
	def csv(self):
		dialog = ctk.CTkInputDialog(text="Ingrese el nombre del archivo", title="Guardar como csv")
		text = dialog.get_input()
		if text is not None:
			if not text.endswith(".csv"):
				text = f"{text}.csv"
			self.df.to_csv(text, index=False)
			messagebox.showinfo("Información", f"Se ha guardado el archivo como {text}")