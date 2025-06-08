import webbrowser
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable
from pathlib import Path

from .lang import tr

class Sponsor:
    """Sponsor dialog to support the project."""
    
    def __init__(self, parent: tk.Tk):
        """Initialize the Sponsor dialog.
        
        Args:
            parent: The parent window
        """
        self.parent = parent
        self.dialog: Optional[tk.Toplevel] = None
        
        # Sponsor links
        self.links = {
            'github': {
                'text': tr('sponsor_github'),
                'url': 'https://github.com/sponsors/Nsfr750',
                'icon': '🐙'  # Placeholder for actual icon
            },
            'paypal': {
                'text': tr('donate_paypal'),
                'url': 'https://paypal.me/3dmega',
                'icon': '💳'  # Placeholder for actual icon
            },
            'patreon': {
                'text': tr('support_patreon'),
                'url': 'https://www.patreon.com/Nsfr750',
                'icon': '🎗️'  # Placeholder for actual icon
            }
        }
    
    def show_sponsor(self) -> None:
        """Show the sponsor dialog."""
        if self.dialog is not None and self.dialog.winfo_exists():
            self.dialog.lift()
            return
            
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(tr('sponsor'))
        self.dialog.geometry('500x400')
        self.dialog.minsize(400, 300)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center the dialog on the parent window
        window_width = 500
        window_height = 400
        screen_width = self.dialog.winfo_screenwidth()
        screen_height = self.dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Main container
        container = ttk.Frame(self.dialog, padding="20")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header = ttk.Label(
            container,
            text=tr('support_development'),
            font=('Helvetica', 16, 'bold'),
            wraplength=400,
            justify=tk.CENTER
        )
        header.pack(pady=(0, 20))
        
        # Message
        message = ttk.Label(
            container,
            text=tr('sponsor_message'),
            wraplength=400,
            justify=tk.CENTER
        )
        message.pack(pady=(0, 30))
        
        # Buttons frame
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Add sponsor buttons
        for key, data in self.links.items():
            self._create_sponsor_button(btn_frame, data)
        
        # Close button
        close_btn = ttk.Button(
            container,
            text=tr('close'),
            command=self.dialog.destroy
        )
        close_btn.pack(side=tk.BOTTOM, pady=(20, 0))
        
        # Make dialog modal
        self.dialog.wait_window(self.dialog)
    
    def _create_sponsor_button(self, parent: ttk.Frame, data: Dict[str, str]) -> None:
        """Create a sponsor button.
        
        Args:
            parent: The parent frame
            data: Button data containing text, url and icon
        """
        btn = ttk.Button(
            parent,
            text=f"{data['icon']} {data['text']}",
            command=lambda url=data['url']: self._open_url(url),
            style='Accent.TButton',
            padding=10
        )
        btn.pack(fill=tk.X, pady=5)
    
    @staticmethod
    def _open_url(url: str) -> None:
        """Open a URL in the default web browser.
        
        Args:
            url: The URL to open
        """
        try:
            webbrowser.open_new_tab(url)
        except Exception as e:
            print(f"Error opening URL {url}: {e}")
