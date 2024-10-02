import customtkinter as ctk
from constants import *
from tkinter import filedialog
from abc import ABC, abstractmethod
from video_import_container import ContainerOblique, ContainerVertical

class VideoInput(ctk.CTkFrame, ABC):
	def __init__(self, parent):
		super().__init__(parent, fg_color= DARKER_GRAY, corner_radius= 30)
		self.grid(column= 0, row= 0, columnspan= 1, sticky= "news", padx= 40, pady= 40)
		self.parent = parent
		lbl = ctk.CTkLabel(self, text= "Click here to import a video",
												font= ctk.CTkFont(family= "Robot", size= 40, weight= "bold"),
												text_color= LIGHT_GRAY, fg_color= DARKER_GRAY, bg_color= DARKER_GRAY,
												justify= "center",
												wraplength= 300)
		lbl.place(relx= 0.5, rely= 0.5, anchor= "center", relwidth= 1, relheight= 1)
		lbl.bind("<Button>", lambda _: self.open_vid())
	
	def open_vid(self):
		path = ""
		try:
			path = filedialog.askopenfile(filetypes=[("Video Files", "*.mp4;*.MOV;")]).name
			self.track(path)
		except AttributeError:
			pass
	
	@abstractmethod
	def track(self, path):
		pass

class VideoObliqueInput(VideoInput):
	def __init__(self, parent):
		super().__init__(parent)

	def track(self, path):
		self.container = ContainerOblique(self.parent, path)
		self.parent.clear_screen_and_place(self.container)

class VideoVerticalInput(VideoInput):
	def __init__(self, parent):
		super().__init__(parent)

	def track(self, path):
		self.container = ContainerVertical(self.parent, path)
		self.parent.clear_screen_and_place(self.container)