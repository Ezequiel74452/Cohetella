import customtkinter as ctk
from img_editor_menu import Container

class Main(ctk.CTk):
	def __init__(self):
		super().__init__()
		ctk.set_appearance_mode("dark")
		self.geometry("1000x600")
		self.title("Rocket tracker")
		self.minsize(800, 500)
		
		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1, uniform="a")
		self.columnconfigure(1, weight= 1, uniform="a")

		self.path = "../Tracker/F-sica-IS---Object-tracker/videos/rojo.MOV"
		Container(self, self.path).grid(row=0, column=0, columnspan=2, sticky="news")
		
		self.mainloop()
	
	def clear_screen_and_place(self, frame):
		self.ob_frame.grid_forget()
		self.ve_frame.grid_forget()
		frame.grid(row=0, column=0, columnspan=2, sticky="news")
	
	def restore_screen(self):
		self.ob_frame.grid(row=0, column=0, columnspan=1, sticky="news", padx=40, pady=40)
		self.ve_frame.grid(row=0, column=1, columnspan=1, sticky="news", padx=40, pady=40)

if __name__ == "__main__":
	Main()