"""
Document management module.

Provides file selection, copying, and cleanup logic decoupled from the
transport layer so that a future GUI version only needs to replace
`select_files()` — everything else stays the same.
"""

import os
import shutil
import tkinter as tk
from tkinter import filedialog

from configs import DOCS_DIR, SUPPORTED_FILETYPES


def select_files() -> list[str]:
    """
    Open a native OS file dialog and return the selected file paths.

    This is the only function that needs to be swapped out for a GUI version.
    Returns an empty list if the user cancels the dialog.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window, show only the dialog
    root.attributes("-topmost", True)  # Bring dialog to the front

    file_paths = filedialog.askopenfilenames(
        title="Select documents to upload",
        filetypes=SUPPORTED_FILETYPES,
    )

    root.destroy()
    return list(file_paths)


def copy_files_to_docs(file_paths: list[str]) -> list[str]:
    """
    Copy the given files into the docs directory, overwriting duplicates silently.

    Returns the list of filenames (basenames) that were copied.
    """
    os.makedirs(DOCS_DIR, exist_ok=True)
    copied: list[str] = []

    for path in file_paths:
        filename = os.path.basename(path)
        dest = os.path.join(DOCS_DIR, filename)
        shutil.copy2(path, dest)
        copied.append(filename)
        print(f"Copied: {filename}")

    return copied


def select_and_copy_files() -> list[str]:
    """
    Open the file picker, copy selected files to the docs directory, and
    return the list of copied filenames.

    Returns an empty list if the user cancels the dialog.
    """
    paths = select_files()

    if not paths:
        print("No files selected.")
        return []

    return copy_files_to_docs(paths)


def cleanup_docs() -> None:
    """
    Remove all non-hidden files from the docs directory.

    Dotfiles (e.g. .gitkeep) are preserved. Safe to call on interruption
    or at the end of a session.
    """
    if not os.path.isdir(DOCS_DIR):
        return

    removed = 0
    for filename in os.listdir(DOCS_DIR):
        if filename.startswith("."):
            continue
        file_path = os.path.join(DOCS_DIR, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            removed += 1

    print(f"Cleaned up {removed} file(s) from {DOCS_DIR}")
