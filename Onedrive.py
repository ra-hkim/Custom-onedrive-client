import subprocess
import pystray
from PIL import Image
import threading
import sys
import os
from pystray import MenuItem as item
from tkinter import simpledialog, Tk
import time

# ========================
# Configuration
# ========================
MOUNT_PATH = "O:\\"
BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(sys.argv[0])))
ICON_PATH = os.path.join(BASE_DIR, "icon.ico")
CACHE_DIR = os.path.join(os.environ.get('SYSTEMDRIVE', 'C:') + os.sep, 'rclone_cache')

# Default rclone flags (editable in tray)
rclone_options = {
    "vfs_cache_max_size": "48G",
    "vfs_read_chunk_size": "256M",
    "vfs_read_chunk_size_limit": "2G",
    "poll_interval": "10s"
}

MOUNT_PROCESS = None

# ========================
# Functions
# ========================
def build_rclone_command():
    return [
        "rclone", "mount", "onedrive:", MOUNT_PATH,
        "--vfs-cache-mode", "full",
        "--vfs-cache-max-size", rclone_options["vfs_cache_max_size"],
        "--vfs-cache-max-age", "24h",
        "--vfs-read-chunk-size", rclone_options["vfs_read_chunk_size"],
        "--vfs-read-chunk-size-limit", rclone_options["vfs_read_chunk_size_limit"],
        "--cache-dir", CACHE_DIR,
        "--dir-cache-time", "24h",
        "--poll-interval", rclone_options["poll_interval"],
        "--network-mode",
        "--allow-other",
        "--links",  # Added as requested
        "--log-level", "INFO",
        "--fast-list"
    ]

def start_mount(icon=None):
    global MOUNT_PROCESS
    if MOUNT_PROCESS and MOUNT_PROCESS.poll() is None:
        return  # Already running
    try:
        # Create cache directory if it doesn't exist
        os.makedirs(CACHE_DIR, exist_ok=True)
        # Run rclone silently
        MOUNT_PROCESS = subprocess.Popen(
            build_rclone_command(),
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if icon:
            # Wait a moment for mount to initialize
            threading.Thread(target=lambda: delayed_notify(icon, "OneDrive mount started successfully!"), daemon=True).start()
    except Exception as e:
        if icon:
            icon.notify(f"Error starting mount: {e}")

def delayed_notify(icon, message, delay=2):
    time.sleep(delay)
    icon.notify(message)

def stop_mount():
    global MOUNT_PROCESS
    if MOUNT_PROCESS:
        MOUNT_PROCESS.terminate()
        MOUNT_PROCESS.wait()
        MOUNT_PROCESS = None

def remount(icon, item=None):
    stop_mount()
    start_mount(icon)
    if icon:
        icon.notify("OneDrive remounted with updated settings.")

def open_mount_folder(icon, item):
    if os.path.exists(MOUNT_PATH):
        os.startfile(MOUNT_PATH)

def check_status(icon, item):
    if MOUNT_PROCESS and MOUNT_PROCESS.poll() is None:
        status = "OneDrive mount is running"
    else:
        status = "OneDrive mount is not running"
    icon.notify(status)

def configure_options(icon, item):
    # Single dialog to edit all parameters at once
    root = Tk()
    root.withdraw()
    for key in rclone_options:
        value = simpledialog.askstring(
            f"Configure {key}",
            f"Enter value for {key} (current: {rclone_options[key]}):",
            initialvalue=rclone_options[key]
        )
        if value:
            rclone_options[key] = value
    root.destroy()
    remount(icon)

def exit_app(icon, item):
    stop_mount()
    icon.stop()
    # sys.exit() removed to prevent traceback

# ========================
# Tray Menu
# ========================
menu = pystray.Menu(
    item('Open Mount Folder', open_mount_folder),
    item('Check Status', check_status),
    item('Configure Options', configure_options),
    item('Remount', remount),
    item('Exit', exit_app)
)

def setup_tray():
    icon_image = Image.open(ICON_PATH)
    icon = pystray.Icon("OneDriveMount", icon_image, "OneDrive Mount", menu)

    # Start mount after tray icon is running
    def delayed_start():
        time.sleep(1)  # wait for tray icon to initialize
        start_mount(icon)

    threading.Thread(target=delayed_start, daemon=True).start()
    icon.run()

# ========================
# Run
# ========================
if __name__ == "__main__":
    setup_tray()
