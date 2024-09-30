import customtkinter as ctk
from PIL import Image, ImageTk  # Pillow for handling images

# Function to replace the main screen with the new GUI
def switch_to_new_screen():
    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Replace with the new GUI content
    new_gui_screen(root)

# Function to set up the new GUI screen within the existing window
def new_gui_screen(parent):
    # Create a frame for the new screen
    """new_frame = ctk.CTkFrame(parent, corner_radius=0)
    new_frame.pack(fill="both", expand=True)

    # Add a sample label as content (replace with your GUI elements)
    label = ctk.CTkLabel(new_frame, text="Welcome to the new screen!", font=("Arial", 24))
    label.pack(expand=True, pady=20)

    # Add a back button to return to the main screen
    back_button = ctk.CTkButton(new_frame, text="Back", command=setup_main_screen)
    back_button.pack(pady=10)"""

# Function to set up the main screen with two sections
def setup_main_screen():
    # Clear the current screen
    for widget in root.winfo_children():
        widget.destroy()

    # Main frame to hold the two sections
    main_frame = ctk.CTkFrame(root, corner_radius=0)
    main_frame.pack(padx=20, pady=20, fill="both", expand=True)

    # Load images for each section (replace 'path_to_image' with your actual image paths)
    oblique_image = Image.open("img/oblique.png")  # Replace with your image path
    oblique_image = oblique_image.resize((300, 150))
    oblique_photo = ImageTk.PhotoImage(oblique_image)

    vertical_image = Image.open("img/vertical.png")  # Replace with your image path
    vertical_image = vertical_image.resize((300, 150))
    vertical_photo = ImageTk.PhotoImage(vertical_image)

    # Create left section for Oblique Projectile Motion
    left_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    left_frame.grid(row=0, column=0, padx=10, pady=10)

    left_title = ctk.CTkLabel(left_frame, text="↗️ Oblique Projectile Motion", font=("Arial", 18))
    left_title.pack(pady=5)

    left_subtitle = ctk.CTkLabel(left_frame, text="Track the path of objects launched at an angle", font=("Arial", 12))
    left_subtitle.pack(pady=5)

    # Image label that triggers screen switch on click
    left_image_label = ctk.CTkLabel(left_frame, image=oblique_photo, text="")
    left_image_label.pack(pady=10)
    left_image_label.bind("<Button-1>", lambda event: switch_to_new_screen())

    # Create right section for Vertical Projectile Motion
    right_frame = ctk.CTkFrame(main_frame, corner_radius=10)
    right_frame.grid(row=0, column=1, padx=10, pady=10)

    right_title = ctk.CTkLabel(right_frame, text="⬇️ Vertical Projectile Motion", font=("Arial", 18))
    right_title.pack(pady=5)

    right_subtitle = ctk.CTkLabel(right_frame, text="Observe objects falling or launched straight up", font=("Arial", 12))
    right_subtitle.pack(pady=5)

    # Image label that triggers screen switch on click
    right_image_label = ctk.CTkLabel(right_frame, image=vertical_photo, text="")
    right_image_label.pack(pady=10)
    right_image_label.bind("<Button-1>", lambda event: switch_to_new_screen())

    # Adjust grid settings to center elements
    main_frame.columnconfigure(0, weight=1)
    main_frame.columnconfigure(1, weight=1)
    main_frame.rowconfigure(0, weight=1)

# Initialize the main window
root = ctk.CTk()
root.geometry("1000x600")
root.title("Physics Motion Tracker")

# Configure custom theme and appearance mode
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# Set up the main screen initially
setup_main_screen()

# Run the application
root.mainloop()
