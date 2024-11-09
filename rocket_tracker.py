import customtkinter as ctk
from gui.constants import *
from gui.frames.img_frames import ImageFrameOblique, ImageFrameVertical

class Main(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("dark")
		self.geometry("1000x600")
		self.title("Rocket tracker")
		self.minsize(800, 500)
		
		self.rowconfigure(0, weight= 1)
		self.columnconfigure((0,1), weight= 1, uniform="a")
		
		self.ob_frame = ImageFrameOblique(self,
																		img_path=OBLIQUE_IMG_PATH,
																		restore_func=self.restore_screen,
																		clear_func=self.clear_screen_and_place)
		self.ve_frame = ImageFrameVertical(self,
																		img_path=VERTICAL_IMG_PATH,
																		restore_func=self.restore_screen,
																		clear_func=self.clear_screen_and_place)

		self.bind('<<RestoreMainScreen>>', self.restore_screen)

		self.mainloop()

	def clear_screen_and_place(self, frame):
		self.ob_frame.grid_forget()
		self.ve_frame.grid_forget()
		frame.grid(row=0, column=0, columnspan=2, sticky="news")
	
	def restore_screen(self, _):
		self.ob_frame.grid(row=0, column=0, columnspan=1, sticky="news", padx=40, pady=40)
		self.ve_frame.grid(row=0, column=1, columnspan=1, sticky="news", padx=40, pady=40)

if __name__ == "__main__":
	Main()