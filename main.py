import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from PIL.Image import Resampling

class ImageResizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Resizer & Info Viewer")

        # Set a style and theme for a modern look
        style = ttk.Style()
        # You can try: 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative'
        style.theme_use('clam')

        # Set a consistent font for all ttk widgets
        default_font = ("Segoe UI", 10)
        style.configure(".", font=default_font)
        style.configure("TLabel", padding=5)
        style.configure("TButton", padding=5)

        # Variables
        self.image_path = None
        self.original_image = None
        self.resized_image = None

        # Variables for width & height entries
        self.width_var = tk.StringVar()
        self.height_var = tk.StringVar()

        # Create main container frames
        self.create_menu()
        
        # Top-level frame inside the root window
        main_frame = ttk.Frame(self.master, padding=(10,10,10,10))
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Top controls frame (Select Image, Width, Height)
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))

        # "Select Image" Button
        select_button = ttk.Button(top_frame, text="Select Image", command=self.select_image)
        select_button.pack(side=tk.LEFT, padx=(0, 15))

        # Width/Height input fields
        width_label = ttk.Label(top_frame, text="Width:")
        width_label.pack(side=tk.LEFT, padx=(0,5))
        width_entry = ttk.Entry(top_frame, textvariable=self.width_var, width=10)
        width_entry.pack(side=tk.LEFT, padx=(0,15))

        height_label = ttk.Label(top_frame, text="Height:")
        height_label.pack(side=tk.LEFT, padx=(0,5))
        height_entry = ttk.Entry(top_frame, textvariable=self.height_var, width=10)
        height_entry.pack(side=tk.LEFT, padx=(0,10))

        # Info frame: shows image format, mode, size, file size
        info_frame = ttk.Frame(main_frame)
        info_frame.pack(fill=tk.X, pady=(0,10))

        self.info_labels = {
            'format': ttk.Label(info_frame, text="Format: N/A"),
            'mode': ttk.Label(info_frame, text="Color Mode: N/A"),
            'size': ttk.Label(info_frame, text="Size (WxH): N/A"),
            'filesize': ttk.Label(info_frame, text="File Size: N/A")
        }

        # Arrange info labels in a row with uniform spacing
        self.info_labels['format'].pack(side=tk.LEFT, padx=(0,20))
        self.info_labels['mode'].pack(side=tk.LEFT, padx=(0,20))
        self.info_labels['size'].pack(side=tk.LEFT, padx=(0,20))
        self.info_labels['filesize'].pack(side=tk.LEFT, padx=(0,0))

        # A separator to delineate sections
        sep = ttk.Separator(main_frame, orient='horizontal')
        sep.pack(fill=tk.X, pady=5)

        # Preview Frame with canvas and scrollbars
        preview_frame = ttk.Frame(main_frame)
        preview_frame.pack(fill=tk.BOTH, expand=True)

        # Canvas for image preview
        self.canvas = tk.Canvas(preview_frame, bg='gray')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbars
        v_scrollbar = ttk.Scrollbar(preview_frame, orient='vertical', command=self.canvas.yview)
        v_scrollbar.pack(side=tk.RIGHT, fill='y')
        h_scrollbar = ttk.Scrollbar(preview_frame, orient='horizontal', command=self.canvas.xview)
        h_scrollbar.pack(side=tk.BOTTOM, fill='x')

        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        # Buttons frame (Resize, Save As, Reset)
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill=tk.X, pady=(10,0))

        resize_button = ttk.Button(buttons_frame, text="Resize", command=self.resize_image)
        resize_button.pack(side=tk.LEFT, padx=(0,10))

        save_button = ttk.Button(buttons_frame, text="Save As", command=self.save_image)
        save_button.pack(side=tk.LEFT, padx=(0,10))

        reset_button = ttk.Button(buttons_frame, text="Reset", command=self.reset)
        reset_button.pack(side=tk.LEFT)

        self.preview_tkimage = None

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.select_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

    def show_about(self):
        messagebox.showinfo("About Image Resizer", 
                            "Image Resizer & Info Viewer\n\n"
                            "A simple tool to view, resize, and save images.\n"
                            "Built with Python, PIL (Pillow), and Tkinter.")

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif"),
                ("All files", "*.*")
            ]
        )
        if file_path:
            try:
                img = Image.open(file_path)
                self.original_image = img
                self.image_path = file_path
                self.update_preview(img)
                self.update_info_panel(img, file_path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image:\n{e}")

    def update_preview(self, img):
        # Display the image at full size (no thumbnail)
        self.preview_tkimage = ImageTk.PhotoImage(img)
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.preview_tkimage)

        # Update the scroll region to match the image size
        width, height = img.size
        self.canvas.config(scrollregion=(0, 0, width, height))

    def update_info_panel(self, img, file_path):
        # Extract image details
        format_str = img.format if img.format else "Unknown"
        mode_str = img.mode if img.mode else "Unknown"
        width, height = img.size
        size_str = f"{width}x{height}"

        # File size
        try:
            file_bytes = os.path.getsize(file_path)
            # Convert bytes to a more readable unit
            if file_bytes < 1024:
                filesize_str = f"{file_bytes} B"
            elif file_bytes < 1024**2:
                filesize_str = f"{file_bytes/1024:.2f} KB"
            else:
                filesize_str = f"{file_bytes/(1024**2):.2f} MB"
        except:
            filesize_str = "N/A"

        self.info_labels['format'].config(text=f"Format: {format_str}")
        self.info_labels['mode'].config(text=f"Color Mode: {mode_str}")
        self.info_labels['size'].config(text=f"Size (WxH): {size_str}")
        self.info_labels['filesize'].config(text=f"File Size: {filesize_str}")

    def resize_image(self):
        if self.original_image is None:
            messagebox.showwarning("No Image", "Please select an image first.")
            return

        width_str = self.width_var.get()
        height_str = self.height_var.get()

        if not (width_str.isdigit() and height_str.isdigit()):
            messagebox.showerror("Invalid Dimensions", "Width and Height must be positive integers.")
            return

        new_width = int(width_str)
        new_height = int(height_str)

        if new_width <= 0 or new_height <= 0:
            messagebox.showerror("Invalid Dimensions", "Width and Height must be greater than 0.")
            return

        # Resize the image using a high-quality filter
        try:
            self.resized_image = self.original_image.resize((new_width, new_height), Resampling.LANCZOS)
            self.update_preview(self.resized_image)
            # Update info panel with new dimensions (file size remains old until saved)
            self.info_labels['size'].config(text=f"Size (WxH): {new_width}x{new_height}")
            messagebox.showinfo("Success", "Image resized successfully. You may now save it.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to resize image:\n{e}")

    def save_image(self):
        if self.resized_image is None:
            messagebox.showwarning("No Resized Image", "Please resize the image before saving.")
            return

        file_types = [
            ("JPEG", "*.jpg"),
            ("PNG", "*.png"),
            ("BMP", "*.bmp"),
            ("TIFF", "*.tiff")
        ]
        save_path = filedialog.asksaveasfilename(
            title="Save Image As",
            defaultextension=".png",
            filetypes=file_types
        )
        if save_path:
            try:
                self.resized_image.save(save_path)
                messagebox.showinfo("Saved", f"Image saved successfully at:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save image:\n{e}")

    def reset(self):
        self.image_path = None
        self.original_image = None
        self.resized_image = None
        self.width_var.set("")
        self.height_var.set("")
        self.preview_tkimage = None
        self.canvas.delete("all")
        self.canvas.config(scrollregion=(0,0,0,0))
        # Reset info panel
        self.info_labels['format'].config(text="Format: N/A")
        self.info_labels['mode'].config(text="Color Mode: N/A")
        self.info_labels['size'].config(text="Size (WxH): N/A")
        self.info_labels['filesize'].config(text="File Size: N/A")

def main():
    root = tk.Tk()
    root.geometry("900x600")  # Comfortable starting size
    root.minsize(800, 500)
    app = ImageResizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
