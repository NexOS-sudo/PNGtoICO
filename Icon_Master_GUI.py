# Icon_Master_GUI.py (Bootstrapper Version)

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, colorchooser
import os
import sys
import subprocess
import logging
import requests
from PIL import Image

# Import the backend class from the separate file
from Icon_Converter_Algorithm import IconConverter

APP_VERSION = "1.1.0"
# This points to the JSON file that contains links to BOTH the app and the updater
VERSION_INFO_URL = "https://raw.githubusercontent.com/JailbreakHubOfficial/PNGtoICO/autoupdater/version.json"


class TextboxHandler(logging.Handler):
    def __init__(self, textbox):
        super().__init__()
        self.textbox = textbox

    def emit(self, record):
        msg = self.format(record)
        self.textbox.configure(state="normal")
        self.textbox.insert("end", msg + "\n")
        self.textbox.configure(state="disabled")
        self.textbox.see("end")
        self.textbox.update_idletasks()


class IconMasterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title(f"Icon Master GUI v{APP_VERSION}")
        self.geometry("800x600")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.folder_icon = ctk.CTkImage(Image.open(self._resource_path("assets/folder_icon.png")))
        self.save_icon = ctk.CTkImage(Image.open(self._resource_path("assets/save_icon.png")))
        self.palette_icon = ctk.CTkImage(Image.open(self._resource_path("assets/palette_icon.png")))
        self.magic_wand_icon = ctk.CTkImage(Image.open(self._resource_path("assets/magic_wand_icon.png")))
        self.update_icon = ctk.CTkImage(Image.open(self._resource_path("assets/update_icon.png")))
        self.input_file_path = tk.StringVar()
        self.output_file_path = tk.StringVar()
        self.subject_color_hex = tk.StringVar(value="#42D6FF")
        self.tolerance_value = tk.IntVar(value=120)
        self._create_widgets()
        self._setup_logging()

    def _resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    def _run_updater(self):
    """
    Downloads and runs the LATEST autoupdater.exe.
    """
    logging.info("Checking for updates...")
    try:
        cert_path = self._resource_path('cacert.pem')
        os.environ['REQUESTS_CA_BUNDLE'] = cert_path

        response = requests.get(VERSION_INFO_URL, timeout=15)
        data = response.json()
        # This URL should now point to autoupdater.exe
        autoupdater_url = data["autoupdater_url"]

        logging.info(f"Downloading latest updater from {autoupdater_url}...")
        updater_response = requests.get(autoupdater_url, timeout=60) # Increased timeout for .exe
        updater_response.raise_for_status()

        # FIXED: Save as autoupdater.exe in the main app directory
        if getattr(sys, 'frozen', False):
            executable_dir = os.path.dirname(sys.executable)
        else:
            executable_dir = os.path.dirname(os.path.abspath(__file__))

        updater_path = os.path.join(executable_dir, 'autoupdater.exe')
        with open(updater_path, 'wb') as f:
            f.write(updater_response.content)
        logging.info("Updater executable downloaded successfully.")

        # FIXED: Launch the .exe directly. No need for sys.executable.
        logging.info("Relaunching via updater...")
        subprocess.Popen([updater_path, APP_VERSION], cwd=executable_dir)
        self.destroy() # Close the main GUI

    except Exception as e:
        logging.error(f"Failed to check for updates: {e}")

    def _create_widgets(self):
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        main_frame.grid_columnconfigure((0, 1), weight=1)
        file_frame = ctk.CTkFrame(main_frame)
        file_frame.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        file_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(file_frame, text="File Setup", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0,
                                                                                                   columnspan=2,
                                                                                                   padx=15,
                                                                                                   pady=(15, 10),
                                                                                                   sticky="w")
        ctk.CTkLabel(file_frame, text="Input Image").grid(row=1, column=0, columnspan=2, padx=15, pady=(5, 0),
                                                          sticky="w")
        ctk.CTkEntry(file_frame, textvariable=self.input_file_path, state="readonly").grid(row=2, column=0, padx=15,
                                                                                           pady=5, sticky="ew")
        ctk.CTkButton(file_frame, text="Browse", image=self.folder_icon, command=self._select_input_file).grid(row=2,
                                                                                                               column=1,
                                                                                                               padx=(
                                                                                                               0, 15),
                                                                                                               pady=5)
        ctk.CTkLabel(file_frame, text="Output (.ico)").grid(row=3, column=0, columnspan=2, padx=15, pady=(5, 0),
                                                            sticky="w")
        ctk.CTkEntry(file_frame, textvariable=self.output_file_path).grid(row=4, column=0, padx=15, pady=(5, 20),
                                                                          sticky="ew")
        ctk.CTkButton(file_frame, text="Save As", image=self.save_icon, command=self._select_output_file).grid(row=4,
                                                                                                               column=1,
                                                                                                               padx=(
                                                                                                               0, 15),
                                                                                                               pady=(
                                                                                                               5, 20))
        controls_frame = ctk.CTkFrame(main_frame)
        controls_frame.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        controls_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(controls_frame, text="Cropping Controls", font=ctk.CTkFont(size=16, weight="bold")).grid(row=0,
                                                                                                              column=0,
                                                                                                              columnspan=3,
                                                                                                              padx=15,
                                                                                                              pady=(
                                                                                                              15, 10),
                                                                                                              sticky="w")
        ctk.CTkLabel(controls_frame, text="Subject Color").grid(row=1, column=0, columnspan=3, padx=15, pady=(5, 0),
                                                                sticky="w")
        self.color_preview_label = ctk.CTkLabel(controls_frame, text="", fg_color=self.subject_color_hex.get(),
                                                width=35, height=35, corner_radius=8)
        self.color_preview_label.grid(row=2, column=0, padx=15, pady=5, sticky="w")
        color_buttons_frame = ctk.CTkFrame(controls_frame, fg_color="transparent")
        color_buttons_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky="w")
        ctk.CTkButton(color_buttons_frame, text="Pick", image=self.palette_icon, command=self._pick_subject_color,
                      width=100).pack(side="left", padx=5)
        ctk.CTkButton(color_buttons_frame, text="Auto", image=self.magic_wand_icon, command=self._auto_detect_color,
                      width=100).pack(side="left", padx=5)
        ctk.CTkLabel(controls_frame, text="Tolerance").grid(row=3, column=0, columnspan=3, padx=15, pady=(10, 0),
                                                            sticky="w")
        ctk.CTkSlider(controls_frame, from_=0, to=255, variable=self.tolerance_value,
                      command=self._update_tolerance_label).grid(row=4, column=0, columnspan=2, padx=15, pady=(5, 20),
                                                                 sticky="ew")
        self.tolerance_label = ctk.CTkLabel(controls_frame, text=f"{self.tolerance_value.get()}", width=40)
        self.tolerance_label.grid(row=4, column=2, padx=(0, 15), pady=(5, 20))
        ctk.CTkButton(self, text="Create Icon", command=self._run_conversion, height=50,
                      font=ctk.CTkFont(size=18, weight="bold")).grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.status_textbox = ctk.CTkTextbox(self, state="disabled", wrap="word",
                                             font=ctk.CTkFont(family="monospace", size=13))
        self.status_textbox.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        update_button = ctk.CTkButton(self, text="", image=self.update_icon, command=self._run_updater, width=32,
                                      height=32, fg_color="transparent", hover_color="#333333")
        update_button.place(relx=1.0, rely=1.0, x=-20, y=-20, anchor="se")

    def _setup_logging(self):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        logger.handlers = []
        handler = TextboxHandler(self.status_textbox)
        formatter = logging.Formatter('[%(levelname)s] %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    def _select_input_file(self):
        file_path = filedialog.askopenfilename(title="Select an Image",
                                               filetypes=(("Image Files", "*.png *.jpg *.jpeg"), ("All files", "*.*")))
        if file_path:
            self.input_file_path.set(file_path)
            base, _ = os.path.splitext(file_path)
            self.output_file_path.set(base + ".ico")
            logging.info(f"Selected input: {os.path.basename(file_path)}")

    def _select_output_file(self):
        file_path = filedialog.asksaveasfilename(title="Save Icon As", defaultextension=".ico",
                                                 filetypes=(("Icon files", "*.ico"),))
        if file_path: self.output_file_path.set(file_path)

    def _pick_subject_color(self):
        color_code = colorchooser.askcolor(title="Choose subject color")
        if color_code and color_code[1]:
            self.subject_color_hex.set(color_code[1])
            self.color_preview_label.configure(fg_color=color_code[1])
            logging.info(f"Set subject color to: {color_code[1]}")

    def _auto_detect_color(self):
        input_p = self.input_file_path.get()
        if not input_p:
            logging.error("Please select an input image first.")
            return
        try:
            logging.info("--- Auto-Detecting Color ---")
            converter = IconConverter(input_p)
            dominant_rgb = converter.find_dominant_color()
            if dominant_rgb:
                hex_color = f"#{dominant_rgb[0]:02x}{dominant_rgb[1]:02x}{dominant_rgb[2]:02x}"
                self.subject_color_hex.set(hex_color)
                self.color_preview_label.configure(fg_color=hex_color)
        except Exception as e:
            logging.error(f"An error occurred during auto-detection: {e}")

    def _update_tolerance_label(self, value):
        self.tolerance_label.configure(text=f"{int(value)}")

    def _run_conversion(self):
        input_p, output_p = self.input_file_path.get(), self.output_file_path.get()
        if not input_p or not output_p:
            logging.error("Please select both input and output files.")
            return
        try:
            color_hex = self.subject_color_hex.get().lstrip('#')
            subject_rgb = tuple(int(color_hex[i:i + 2], 16) for i in (0, 2, 4))
            logging.info("--- Starting Conversion ---")
            converter = IconConverter(input_p)
            converter.convert(
                output_path=output_p,
                subject_color=subject_rgb,
                tolerance=self.tolerance_value.get()
            )
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    app = IconMasterApp()
    app.mainloop()

