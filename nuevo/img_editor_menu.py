import customtkinter as ctk
import cv2
from abc import ABC, abstractmethod
from close_btn import CloseBtn
from img_editor_panels import OrigenPanel, FPSPanel
from img_output import ImageFrameOutput
from PIL import Image, ImageTk, ImageDraw
from tkinter import messagebox
from tracks import oblique_track, vertical_track
from utilsGraficas import oblique_graph, graficar_plotly

class Container(ctk.CTkFrame, ABC):
	def __init__(self, parent, path):
		super().__init__(parent)
		self.rowconfigure(0, weight= 1)
		self.columnconfigure(0, weight= 1, uniform= "a")
		self.columnconfigure(1, weight= 3, uniform= "a")

		self.path = path
		self.selection_enabled = False
		self.canvas_w = 0
		self.canvas_h = 0
		self.img_w = 0
		self.img_h = 0
		
		self.read_first_frame()

	def read_first_frame(self):
		cap = cv2.VideoCapture(self.path)
		_, frame = cap.read()
		frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		self.original_img = Image.fromarray(frame_rgb)
		self.img = self.original_img
		self.img_ratio = self.img.size[0]/self.img.size[1]
		self.img_tk = ImageTk.PhotoImage(self.img)
		self.img_output = ImageFrameOutput(self, self.resize_img, self.select_pixel)
		self.img_output.grid(column= 1, row= 0, columnspan=1, sticky= "news", padx= 15, pady= 15)
		self.close_btn = CloseBtn(parent= self, func= self.close_btn_func)
		self.create_menu()

	@abstractmethod
	def create_menu(self):
		pass

	def close_btn_func(self):
		pass

	def resize_img(self, event):
		self.canvas_h = event.height
		self.canvas_w = event.width
		canvas_ratio = self.canvas_w / self.canvas_h
		if canvas_ratio > self.img_ratio:
			self.img_h = self.canvas_h
			self.img_offset_y = 0
			self.img_w = self.img_ratio * self.img_h
			self.img_offset_x = (self.canvas_w-self.img_w) / 2
		else:
			self.img_w = self.canvas_w
			self.img_offset_x = 0
			self.img_h = self.img_w / self.img_ratio
			self.img_offset_y = (self.canvas_h-self.img_h) / 2
		self.place_img()

	def place_img(self):
		self.img_tk = ImageTk.PhotoImage(self.img.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w/2, self.canvas_h/2, image= self.img_tk)

	def select_pixel(self, event):
		if not self.selection_enabled:
			return
		x = (event.x - self.img_offset_x) * (self.original_img.size[0] / self.img_tk.width())
		y = (event.y - self.img_offset_y) * (self.original_img.size[1] / self.img_tk.height())
		if 0 <= x < self.original_img.size[0] and 0 <= y < self.original_img.size[1]:
			self.menu.frame.origin.updateX(str(round(x)))
			self.menu.frame.origin.updateY(str(round(y)))
			self.draw_cross(x, y)
			self.disable_pixel_selection()

	def draw_cross(self, x, y):
		self.img_display = self.original_img.copy()
		draw = ImageDraw.Draw(self.img_display)
		cross_size = 10
		draw.line((x - cross_size, y, x + cross_size, y), fill="red", width=2)
		draw.line((x, y - cross_size, x, y + cross_size), fill="red", width=2)
		self.refresh_img()

	def refresh_img(self):
		self.img_tk = ImageTk.PhotoImage(self.img_display.resize((int(self.img_w), int(self.img_h))))
		self.img_output.delete("all")
		self.img_output.create_image(self.canvas_w/2, self.canvas_h/2, image= self.img_tk)


	def enable_pixel_selection(self):
		self.selection_enabled = True

	def disable_pixel_selection(self):
		self.selection_enabled = False

class ContainerVertical(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuVertical(self, self.enable_pixel_selection, self.path)

class ContainerOblique(Container):
	def __init__(self, parent, path):
		super().__init__(parent, path)
	
	def create_menu(self):
		self.menu = MenuOblique(self, self.enable_pixel_selection, self.path)

class Menu(ctk.CTkTabview, ABC):
	def __init__(self, parent, func, path):
		super().__init__(parent)
		self.grid(column= 0, row= 0, sticky= "news")
		self.func = func
		self.path = path
	
	@abstractmethod
	def create_tab(self):
		pass

class MenuVertical(Menu):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
		self.add("Menú")
		self.create_tab()
	
	def create_tab(self):
		self.frame = TrackFrameVertical(self.tab("Menú"), self.func, self.path)

class MenuOblique(Menu):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
		self.add("Menú")
		self.create_tab()
	
	def create_tab(self):
		self.frame = TrackFrameOblique(self.tab("Menú"), self.func, self.path)

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
			SuccesfulTrackFrame(root, df)

class TrackFrameOblique(TrackFrame):
	def __init__(self, parent, func, path):
		super().__init__(parent, func, path)
	
	def track(self):
		df = oblique_track(self.path, self.Y.get(), self.X.get(), self.FPS.get())
		if df is not None:
			root = self.winfo_toplevel()
			for widget in root.winfo_children():
				widget.destroy()
			SuccesfulTrackFrame(root, df)

class SuccesfulTrackFrame(ctk.CTkFrame, ABC):
	def __init__(self, parent, df):
		super().__init__(parent)
		self.grid(column= 0, row= 0, columnspan= 2, sticky= "news", padx= 10, pady= 10)
		self.df = df
		self.columnconfigure(0, weight=1)
		# Título
		self.title_label = ctk.CTkLabel(
			self, 
			text="El video se ha trackeado correctamente", 
			font=ctk.CTkFont(size=24, weight="bold"),
			text_color="green"  # Color del texto
		)
		self.title_label.grid(row=0, padx=20, pady=(20, 10), sticky="nsew")

		# Botón 1
		self.button1 = ctk.CTkButton(
			self, 
			text="Graficar", 
			command=self.graph, 
			fg_color="lightgreen", 
			hover_color="green"
		)
		self.button1.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

		# Botón 2
		self.button2 = ctk.CTkButton(
			self, 
			text="Guardar como csv", 
			command=self.csv, 
			fg_color="salmon", 
			hover_color="red"
		)
		self.button2.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

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
		graficar_plotly(self.df)

class SuccesfulTrackFrameOblique(SuccesfulTrackFrame):
	def __init__(self, parent, df):
		super().__init__(parent, df)

	def graph(self):
		oblique_graph(self.df)