import os
import tkinter as tk
from tkinter import filedialog

def open_exe_from_explorer():
    """Opens an .exe file selected by the user from the file explorer."""

    file_path = filedialog.askopenfilename(filetypes=[("Executable Files", "*.exe")])

    if file_path:
        os.startfile(file_path)

# Create a simple GUI window
root = tk.Tk()
root.withdraw()  # Hide the main window

# Trigger the file selection dialog
open_exe_from_explorer()

root.mainloop()  # Keep the script running (though the main window is hidden)