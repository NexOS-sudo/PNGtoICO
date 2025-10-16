# autoupdater.py (Updated for EXE compilation)

import requests
import os
import sys
import subprocess
import shutil
import zipfile
import io
import time
import traceback

VERSION_INFO_URL = "https://raw.githubusercontent.com/JailbreakHubOfficial/PNGtoICO/autoupdater/version.json"
MAIN_APP_EXE = "Icon_Master_GUI.exe"

# The updater must also ignore itself when compiled
FILES_TO_IGNORE = (
    "autoupdater.py",
    "autoupdater.exe"
)


def _resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath("..")
    return os.path.join(base_path, relative_path)


def log_error(version):
    # ... (unchanged)
    with open("autoupdater_error.log", "w", encoding="utf-8") as error_file:
        error_file.write(f"Icon Master Autoupdater (for v{version})\n---\n")
        traceback.print_exc(file=error_file)
    traceback.print_exc()
    print("\n[!!!] An error occurred. See autoupdater_error.log for details.")


def main():
    print("--- Icon Master Auto-Updater ---")
    if len(sys.argv) < 2:
        print("Error: Current version not provided.")
        time.sleep(5)
        return
    current_version = sys.argv[1]
    print(f"Current version: {current_version}")

    try:
        print("Checking for new updates...")
        response = requests.get(VERSION_INFO_URL, timeout=15)
        response.raise_for_status()
        data = response.json()
        latest_version = data["version"]
        download_url = data["url"]
        print(f"Latest version available: {latest_version}")

        if latest_version == current_version:
            print("You are already on the latest version.")
            time.sleep(3)
            # Relaunch the original app if it exists
            if os.path.exists(MAIN_APP_EXE):
                subprocess.Popen(MAIN_APP_EXE)
            sys.exit()

        print(f"Downloading new version from: {download_url}")
        response = requests.get(download_url, timeout=60)
        response.raise_for_status()
        zip_in_memory = io.BytesIO(response.content)

        print("Download complete. Extracting files...")
        with zipfile.ZipFile(zip_in_memory) as zf:
            extracted_folder_name = zf.namelist()[0]
            zf.extractall()

        print(f"Extracted to: {extracted_folder_name}")
        time.sleep(1)

        print("Replacing old application files...")
        for item in os.listdir(".."):
            if item in FILES_TO_IGNORE or item == extracted_folder_name:
                continue
            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Warning: Could not remove {item}. {e}")

        print("Old files removed. Installing new version...")
        for item in os.listdir(extracted_folder_name):
            shutil.move(os.path.join(extracted_folder_name, item), "..")
        os.rmdir(extracted_folder_name)

        print("\nUpdate successful!")

    except Exception:
        log_error(current_version)
        time.sleep(10)
        sys.exit(1)

    print(f"Relaunching application in 3 seconds...")
    time.sleep(3)
    # Launch the newly updated executable
    if os.path.exists(MAIN_APP_EXE):
        subprocess.Popen(MAIN_APP_EXE)
    sys.exit(0)


if __name__ == "__main__":
    main()