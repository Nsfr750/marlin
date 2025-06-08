import tkinter as tk
from tkinter import ttk
from pathlib import Path
from typing import Optional

from .version import get_version
from .lang import tr

class About:
    """About dialog showing application information and version."""
    
    @staticmethod
    def show_about(parent: tk.Tk) -> None:
        """Show the About dialog.
        
        Args:
            parent: The parent window
        """
        about_dialog = tk.Toplevel(parent)
        about_dialog.title(tr('about'))
        about_dialog.geometry('400x300')
        about_dialog.resizable(False, False)
        about_dialog.transient(parent)
        about_dialog.grab_set()
        
        # Center the dialog on the parent window
        window_width = 400
        window_height = 300
        screen_width = about_dialog.winfo_screenwidth()
        screen_height = about_dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        about_dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Main container
        container = ttk.Frame(about_dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # App title
        title_label = ttk.Label(
            container,
            text=tr('app_title'),
            font=('Helvetica', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Version
        version_label = ttk.Label(
            container,
            text=f"{tr('version')} {get_version()}",
            font=('Helvetica', 10)
        )
        version_label.pack(pady=(0, 20))
        
        # Description
        desc_frame = ttk.LabelFrame(container, text=tr('about_project'), padding=10)
        desc_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        desc_text = tk.Text(
            desc_frame,
            wrap=tk.WORD,
            width=40,
            height=6,
            font=('Helvetica', 9),
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=0
        )
        desc_text.insert('1.0', tr('about_description'))
        desc_text.config(state=tk.DISABLED)
        desc_text.pack(fill=tk.BOTH, expand=True)
        
        # Copyright
        copyright_label = ttk.Label(
            container,
            text=" 2025 Nsfr750 - All Rights Reserved",
            font=('Helvetica', 8)
        )
        copyright_label.pack(side=tk.BOTTOM, pady=(10, 0))
        
        # Close button
        close_btn = ttk.Button(
            container,
            text=tr('close'),
            command=about_dialog.destroy
        )
        close_btn.pack(side=tk.BOTTOM, pady=(10, 0))
        
        # Make dialog modal
        about_dialog.wait_window(about_dialog)
