import customtkinter as ctk
import pandas as pd
import os
import webbrowser
from abc import ABC, abstractmethod
from constants import *
from tkinter import filedialog, messagebox
from utilsGraficas import graficar_csv_plotly, oblique_graph

class CSVInput(ctk.CTkFrame, ABC):
	def __init__(self, parent):
		super().__init__(parent, fg_color= DARKER_GRAY, corner_radius= 30)
		self.grid(column= 1, row= 0, columnspan= 1, sticky= "news", padx= 40, pady= 40)
		lbl = ctk.CTkLabel(self, text= "Click here to load a .csv file",
												font= ctk.CTkFont(family= "Robot", size= 40, weight= "bold"),
												text_color= LIGHT_GRAY, fg_color= DARKER_GRAY, bg_color= DARKER_GRAY,
												justify= "center",
												wraplength= 300)
		lbl.place(relx= 0.5, rely= 0.5, anchor= "center", relwidth= 1, relheight= 1)
		lbl.bind("<Button>", lambda _: self.load_csv())

	def load_csv(self):
		path = ""
		try:
			path = filedialog.askopenfile(filetypes=[("CSV Files", "*.csv")]).name
			self.graficar(path)
		except AttributeError:
			pass

	@abstractmethod
	def graficar(self, path):
		pass

class CSVVerticalInput(CSVInput):
	def __init__(self, parent):
		super().__init__(parent)

	def graficar(self, path):
		path_to_html = graficar_csv_plotly(path)
		response = messagebox.askyesno(
			"Confirmar",
			"Se ha generado el HTML con éxito ¿Desea abrirlo en el navegador?"
    )
		if response:
			file_url = 'file://' + os.path.abspath(path_to_html).replace('\\', '/')
			webbrowser.open(file_url)

class CSVObliqueInput(CSVInput):
	def __init__(self, parent):
		super().__init__(parent)
	
	def graficar(self, path):
		df = pd.read_csv(path)
		oblique_graph(df)