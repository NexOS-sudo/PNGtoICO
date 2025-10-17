# IconMaster 🎨

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

![IconMaster Project Logo](Project's Logo/IconMaster-Logo.jpg?width=550)

**IconMaster** is a modern, standalone desktop application for converting PNG images into ICO files with a single click. Built with Python and CustomTkinter for a sleek and simple user experience.

---

## Table of Contents

- [About The Project](#about-the-project)
  - [Features](#features)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [For End-Users (Recommended)](#for-end-users-recommended)
  - [For Developers](#for-developers)
- [Usage](#usage)
- [Building the Executable](#building-the-executable)
- [License](#license)

---

## About The Project

IconMaster was created to solve a simple problem: the need for a quick, offline tool to create `.ico` files from `.png` images. This is especially useful for developers who need to generate icons for their Windows applications. The app is lightweight, requires no installation, and has a clean, modern interface.

### Features

* **Simple & Fast:** Convert images in just two clicks.
* **Modern GUI:** A visually appealing interface that's easy to navigate.
* **Standalone:** Runs as a single `.exe` file without needing any dependencies or installation.
* **High-Quality Output:** Uses the Pillow library to ensure a quality conversion.

### Built With

This project relies on these excellent open-source libraries:

* [Python](https://www.python.org/)
* [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
* [Pillow (PIL)](https://python-pillow.org/)

---

## Getting Started

You can either download the ready-to-use application or run the project from the source code.

### For End-Users (Recommended)

1.  Navigate to the [**Releases**](https://github.com/NexOS-sudo/PNGtoICO/releases) page of this repository.
2.  Download the latest `Icon_Master_GUI.exe` file.
3.  Run the file. No installation is required.

### For Developers

To run this project from the source code, you'll need Python and `pip` installed.

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/NexOS-sudo/PNGtoICO.git](https://github.com/NexOS-sudo/PNGtoICO.git)
    cd PNGtoICO
    ```

2.  **Install the required packages:**
    ```sh
    pip install customtkinter pillow
    ```

3.  **Run the application:**
    ```sh
    python Icon_Master_GUI.py
    ```

---

## Usage

1.  Launch the `Icon_Master_GUI.exe` application.
2.  Click the **"Select PNG Image"** button.
3.  Choose your desired `.png` file from the file dialog.
4.  The application will automatically process it and save the new `.ico` file in the **same directory** as the original image. A success message will confirm the conversion.

---

## Building the Executable

If you have modified the source code and wish to compile your own `.exe` file, you can use `PyInstaller`.

1.  **Install PyInstaller:**
    ```sh
    pip install pyinstaller
    ```

2.  **Run the build command from the project's root directory:**
    *This command bundles all necessary assets and scripts into a single executable file.*
    ```sh
    pyinstaller --onefile --windowed --add-data "assets;assets" --add-data "cacert.pem;." --hidden-import "PIL" --hidden-import "customtkinter" Icon_Master_GUI.py Icon_Converter_Algorithm.py
    ```
    *The final `.exe` will be located in the `dist` folder that PyInstaller creates. By default, it will be named `Icon_Master_GUI.exe`.*

---

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.
