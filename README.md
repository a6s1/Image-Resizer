# Image Resizer & Info Viewer

A simple, user-friendly desktop application for viewing and resizing images. It provides image details at a glance before resizing, including format, color mode, dimensions, and file size. With a clean, modern interface built using Python’s Tkinter (with `ttk` widgets) and the Pillow imaging library, this tool makes it easy to quickly inspect and resize images, then save the results in various formats.

![Screenshot of the Image Resizer & Info Viewer application](./screenshot.png)

## Features

- **View Images at Full Size:**  
  No scaling or thumbnailing by default. The selected image is displayed in its actual dimensions, with scrollbars for navigation if it’s larger than your window.

- **Image Metadata Display:**  
  The application shows essential information about the selected image:
  - **Format:** JPEG, PNG, BMP, TIFF, etc.
  - **Color Mode:** RGB, RGBA, L (grayscale), etc.
  - **Dimensions:** Original width and height in pixels.
  - **File Size:** Displayed in a human-readable format (Bytes, KB, or MB).

- **Easy Resizing:**  
  Simply enter your desired width and height, and click **Resize**. The application uses a high-quality Lanczos filter (via Pillow’s `Resampling.LANCZOS`) for smooth resizing.

- **Save Resized Images:**  
  Save the newly resized image in common formats like JPEG, PNG, BMP, or TIFF.

- **Clean and Modern Interface:**  
  Built with `ttk` widgets and a selectable theme, the application has a crisp and professional look. The window layout automatically adapts as you resize it.

- **Integrated Menu:**  
  A simple menubar includes a “File” menu for opening images and exiting the app, as well as a “Help” menu with an “About” dialog.

## Requirements

- **Python 3.6+**  
- **Pillow (PIL fork)** for image processing  
- **Tkinter** (usually included with most Python installations)  
- **PyInstaller (optional)** for packaging into a standalone executable

### Install Dependencies

```bash
pip install Pillow
```

*(Tkinter usually comes with standard Python installations on Windows. On some Linux distributions, you may need to install it via your package manager.)*

## Usage

1. **Run the Application:**
   ```bash
   python main.py
   ```

2. **Open an Image:**
   - Click the **Select Image** button or go to `File > Open Image`.
   - Navigate to your desired image (JPEG, PNG, BMP, TIFF, etc.).

3. **View Details:**
   - Once selected, the image is displayed in full size on the canvas.
   - The info bar above shows the image’s format, color mode, dimensions, and file size.

4. **Resize the Image:**
   - Enter new dimensions in the **Width** and **Height** fields.
   - Click **Resize**. The image and the displayed dimensions will update accordingly.

5. **Save the Resized Image:**
   - Click **Save As** to choose a format and location.
   - The resized image is then saved on your system.

6. **Reset:**
   - Click **Reset** to clear the currently loaded image and restore default fields.

## Packaging into an Executable (Windows)

If you’d like to distribute the tool without requiring end-users to have Python installed:

1. Install PyInstaller:
   ```bash
   pip install PyInstaller
   ```

2. Run PyInstaller on the script:
   ```bash
   pyinstaller --onefile --windowed main.py
   ```

3. After building completes, an executable will be available in the `dist` folder.

## Contributing

Contributions are welcome! If you have suggestions, feature requests, or bug reports, feel free to open an issue or create a pull request.

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/my-new-feature
   ```
3. **Commit your changes:**
   ```bash
   git commit -am 'Add some feature'
   ```
4. **Push to the branch:**
   ```bash
   git push origin feature/my-new-feature
   ```
5. **Create a new Pull Request**

## License

This project is released under the [MIT License](LICENSE).