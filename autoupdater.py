# autoupdater.py

import requests
import os
import sys
import subprocess
import shutil
import zipfile
import io
import time
import traceback

# --- CONFIGURATION ---
# IMPORTANT: You must host a JSON file online (e.g., on GitHub Gist or a raw file)
# that contains the latest version info and a download link.
VERSION_INFO_URL = "https://raw.githubusercontent.com/YourUsername/YourRepo/main/version.json"

# The main GUI script to relaunch after the update
MAIN_APP_SCRIPT = "icon_master_gui.py"

# Files to NOT delete during the update process
FILES_TO_IGNORE = (
    "autoupdater.py",
    # Add any config files or user data files here if you have them
)


def log_error(version):
    """Writes detailed error info to a log file."""
    with open("autoupdater_error.log", "w", encoding="utf-8") as error_file:
        error_file.write(f"Icon Master Autoupdater (for v{version})\n---\n")
        traceback.print_exc(file=error_file)
    traceback.print_exc()
    print("\n[!!!] An error occurred. See autoupdater_error.log for details.")


def main():
    print("--- Icon Master Auto-Updater ---")

    # The GUI passes its current version as an argument
    if len(sys.argv) < 2:
        print("Error: Current version not provided. Run this from the main app.")
        time.sleep(5)
        return

    current_version = sys.argv[1]
    print(f"Current version: {current_version}")

    try:
        # 1. Fetch Latest Version Info
        print("Checking for new updates...")
        response = requests.get(VERSION_INFO_URL, timeout=15)
        response.raise_for_status()  # Raises an error if the request failed
        data = response.json()
        latest_version = data["version"]
        download_url = data["url"]

        print(f"Latest version available: {latest_version}")

        if latest_version == current_version:
            print("You are already on the latest version.")
            time.sleep(3)
            # Relaunch the main app and exit
            subprocess.Popen([sys.executable, MAIN_APP_SCRIPT])
            sys.exit()

        print(f"New version found! Downloading from: {download_url}")

        # 2. Download the New Version
        response = requests.get(download_url, timeout=60)
        response.raise_for_status()
        zip_in_memory = io.BytesIO(response.content)

        print("Download complete. Extracting files...")

        # 3. Extract Files
        with zipfile.ZipFile(zip_in_memory) as zf:
            # Assuming the zip contains files in a root folder, e.g., 'icon_master-1.1.0/'
            extracted_folder_name = zf.namelist()[0]
            zf.extractall()

        print(f"Extracted to: {extracted_folder_name}")
        time.sleep(1)  # Give a moment for file system to catch up

        # 4. Replace Old Files
        print("Replacing old application files... DO NOT CLOSE THIS WINDOW.")

        for item in os.listdir("."):
            if item in FILES_TO_IGNORE or item == extracted_folder_name:
                continue

            try:
                if os.path.isfile(item):
                    os.remove(item)
                elif os.path.isdir(item):
                    shutil.rmtree(item)
            except Exception as e:
                print(f"Warning: Could not remove {item}. {e}")

        print("Old files removed.")

        # 5. Move New Files into Place
        print("Installing new version...")
        for item in os.listdir(extracted_folder_name):
            shutil.move(os.path.join(extracted_folder_name, item), ".")

        # Clean up the empty extracted folder
        os.rmdir(extracted_folder_name)

        print("\nUpdate successful!")

    except Exception:
        log_error(current_version)
        time.sleep(10)
        sys.exit(1)

    # 6. Relaunch the Main App
    print(f"Relaunching {MAIN_APP_SCRIPT} in 3 seconds...")
    time.sleep(3)
    subprocess.Popen([sys.executable, MAIN_APP_SCRIPT])
    sys.exit(0)


if __name__ == "__main__":
    main()