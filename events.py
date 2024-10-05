import tkinter as tk

class ClearAndUpdateMainEvent(tk.Event):
	def __init__(self, frame):
		super().__init__()
		self.frame = frame