import tkinter as tk
import ttkbootstrap as ttk
import pandas as pd
from abc import ABC, abstractmethod

class CSVViewer(tk.Tk, ABC):
	def __init__(self, path):
		super().__init__()
		self.title("CSV Viewer")
		self.geometry("600x400")

		self.df = pd.read_csv(path)

	@abstractmethod
	def mostrarTabla(self):
		pass

class ObliqueCSVViewer(CSVViewer):
	def __init__(self, path):
		super().__init__(path)

		self.table = ttk.Treeview(self, columns = ("T", "PX", "PY", "VX", "VY", "AX", "AY"), show = "headings")
		self.table.heading("T", text = "Tiempo (s)")
		self.table.heading("PX", text = "Posición X (m)")
		self.table.heading("PY", text = "Posición Y (m)")
		self.table.heading("VX", text = "Velocidad X (m/s)")
		self.table.heading("VY", text = "Velocidad Y (m/s)")
		self.table.heading("AX", text = "Aceleración X (m/s^2)")
		self.table.heading("AY", text = "Aceleración Y (m/s^2)")
		self.table.pack(fill = "both", expand = True)

		self.mostrarTabla()
		self.mainloop()

	def mostrarTabla(self):
		for i in reversed(range(len(self.df))):
			self.table.insert(parent = "", index = 0, values = (
				self.df["Tiempo (s)"][i],
				self.df["Posición X (m)"][i], self.df["Posición Y (m)"][i],
				self.df["Velocidad X (m/s)"][i], self.df["Velocidad Y (m/s)"][i],
				self.df["Aceleración X (m/s^2)"][i], self.df["Aceleración Y (m/s^2)"][i]
			))

class VerticalCSVViewer(CSVViewer):
	def __init__(self, path):
		super().__init__(path)

		self.table = ttk.Treeview(self, columns = ("T", "PY", "VY", "AY"), show = "headings")
		self.table.heading("T", text = "Tiempo (s)")
		self.table.heading("PY", text = "Posición Y (m)")
		self.table.heading("VY", text = "Velocidad Y (m/s)")
		self.table.heading("AY", text = "Aceleración Y (m/s^2)")
		self.table.pack(fill = "both", expand = True)

		self.mostrarTabla()
		self.mainloop()

	def mostrarTabla(self):
		for i in reversed(range(len(self.df))):
			self.table.insert(parent = "", index = 0, values = (
				self.df["Tiempo (s)"][i],
				self.df["Posición Y (m)"][i],
				self.df["Velocidad Y (m/s)"][i],
				self.df["Aceleración Y (m/s^2)"][i]
			))