import customtkinter as ctk
from angle_tab_panels import OrigenPanel

class AngleFrame(ctk.CTkFrame):
	def __init__(self, parent, enable_i, enable_s, pasar_frame, path):
		super().__init__(parent, fg_color= "transparent")
		self.pack(expand= True, fill= "both")
		
		self.X_i = ctk.StringVar(value="0")
		self.Y_i = ctk.StringVar(value="0")
		self.X_s = ctk.StringVar(value="0")
		self.Y_s = ctk.StringVar(value="0")
		self.path = path
		self.origin_i = OrigenPanel(self, enable_i, self.X_i, self.Y_i, "extremo inferior")
		self.origin_s = OrigenPanel(self, enable_s, self.X_s, self.Y_s, "extremo superior")
		self.btn = ctk.CTkButton(self, text= "Confirmar y pasar al siguiente frame", command= pasar_frame)
		self.btn.pack(side= "bottom", pady= 10)
	
	def updateX_i(self, value):
		self.origin_i.updateX(value)
	
	def updateY_i(self, value):
		self.origin_i.updateY(value)
	
	def updateX_s(self, value):
		self.origin_s.updateX(value)
	
	def updateY_s(self, value):
		self.origin_s.updateY(value)
