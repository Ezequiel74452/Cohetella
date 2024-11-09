import customtkinter as ctk
from abc import ABC, abstractmethod
from gui.frames.succesful_track_frame import SuccesfulTrackFrameVertical, SuccesfulTrackFrameOblique
from utils.utilsTracks import vertical_track, oblique_track
from gui.video.video_import_frame_panels import OrigenPanel, FPSPanel

class TrackFrame(ctk.CTkFrame, ABC):
	def __init__(self, parent, func, path):
		super().__init__(parent, fg_color= "transparent")
		self.pack(expand= True, fill= "both")
		
		self.X = ctk.StringVar(value="0")
		self.Y = ctk.StringVar(value="0")
		self.FPS = ctk.StringVar(value="")
		self.path = path
		self.func = func
		
		self.origin = OrigenPanel(self, self.func, self.X, self.Y)
		self.fps = FPSPanel(self, self.FPS)
		self.btn = ctk.CTkButton(self, text= "Track",
														command= self.track,
														state= "disabled")
		self.btn.pack(side= "bottom", pady= 10)
		self.enable_button()
	
	def enable_button(self):
		if self.btn._state == "disabled" and self.availability():
				self.btn.configure(state= "normal")
		elif self.btn._state == "normal" and not self.availability():
				self.btn.configure(state= "disabled")
		self.after(10, self.enable_button)
	
	def availability(self):
		return self.FPS.get().isdigit() and self.X.get() and self.Y.get()
	
	@abstractmethod
	def track(self):
		pass

class TrackFrameVertical(TrackFrame):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
	
	def track(self):
		df = vertical_track(self.path, self.Y.get(), self.X.get(), self.FPS.get())
		if df is not None:
			root = self.winfo_toplevel()
			for widget in root.winfo_children():
				widget.destroy()
			SuccesfulTrackFrameVertical(root, df)

class TrackFrameOblique(TrackFrame):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
	
	def track(self):
		df = oblique_track(self.path, self.Y.get(), self.X.get(), self.FPS.get())
		if df is not None:
			root = self.winfo_toplevel()
			for widget in root.winfo_children():
				widget.destroy()
			SuccesfulTrackFrameOblique(root, df)