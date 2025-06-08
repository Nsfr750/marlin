"""
Help Dialog Module

This module provides the Help dialog for the Project.
Displays usage instructions and feature highlights in a tabbed interface.

License: GPL v3.0 (see LICENSE)
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional, Dict, List, Any
from pathlib import Path

from .lang import tr

class Help:
    """Help dialog showing application documentation and usage instructions."""
    
    @staticmethod
    def show_help(parent: tk.Tk) -> None:
        """Show the Help dialog.
        
        Args:
            parent: The parent window
        """
        help_dialog = tk.Toplevel(parent)
        help_dialog.title(tr('help'))
        help_dialog.geometry('800x600')
        help_dialog.minsize(600, 400)
        help_dialog.transient(parent)
        help_dialog.grab_set()
        
        # Center the dialog on the parent window
        window_width = 800
        window_height = 600
        screen_width = help_dialog.winfo_screenwidth()
        screen_height = help_dialog.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        help_dialog.geometry(f'{window_width}x{window_height}+{x}+{y}')
        
        # Create main container
        container = ttk.Frame(help_dialog, padding="10")
        container.pack(fill=tk.BOTH, expand=True)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(container)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add tabs
        tabs = {
            'usage': tr('usage'),
            'features': tr('features'),
            'keyboard': tr('keyboard_shortcuts')
        }
        
        # Create tab frames
        tab_frames = {}
        for tab_id, tab_name in tabs.items():
            tab_frames[tab_id] = ttk.Frame(notebook, padding=10)
            notebook.add(tab_frames[tab_id], text=tab_name)
        
        # Populate tabs
        Help._setup_usage_tab(tab_frames['usage'])
        Help._setup_features_tab(tab_frames['features'])
        Help._setup_shortcuts_tab(tab_frames['keyboard'])
        
        # Close button
        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        
        close_btn = ttk.Button(
            btn_frame,
            text=tr('close'),
            command=help_dialog.destroy
        )
        close_btn.pack(side=tk.RIGHT)
        
        # Make dialog modal
        help_dialog.wait_window(help_dialog)
    
    @staticmethod
    def _setup_usage_tab(parent: ttk.Frame) -> None:
        """Set up the Usage tab content."""
        text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True)
        
        # Insert help text
        help_text = f"""{tr('help_usage')}

{tr('help_installation')}

{tr('help_configuration')}
"""
        text.insert('1.0', help_text)
        text.config(state=tk.DISABLED)
    
    @staticmethod
    def _setup_features_tab(parent: ttk.Frame) -> None:
        """Set up the Features tab content."""
        text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True)
        
        # Insert features text
        features_text = f"""{tr('help_features')}

{tr('help_troubleshooting')}
"""
        text.insert('1.0', features_text)
        text.config(state=tk.DISABLED)
    
    @staticmethod
    def _setup_shortcuts_tab(parent: ttk.Frame) -> None:
        """Set up the Keyboard Shortcuts tab content."""
        # Create a frame with a treeview for shortcuts
        columns = ('action', 'shortcut')
        tree = ttk.Treeview(
            parent,
            columns=columns,
            show='headings',
            selectmode='browse'
        )
        
        # Define columns
        tree.heading('action', text=tr('action'))
        tree.heading('shortcut', text=tr('shortcut'))
        
        # Set column widths
        tree.column('action', width=300, anchor=tk.W)
        tree.column('shortcut', width=150, anchor=tk.W)
        
        # Add scrollbar
        vsb = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        
        # Pack the tree and scrollbar
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add shortcuts data
        shortcuts = [
            (tr('file_open'), 'Ctrl+O'),
            (tr('file_save'), 'Ctrl+S'),
            (tr('file_save_as'), 'Ctrl+Shift+S'),
            (tr('edit_undo'), 'Ctrl+Z'),
            (tr('edit_redo'), 'Ctrl+Y'),
            (tr('edit_cut'), 'Ctrl+X'),
            (tr('edit_copy'), 'Ctrl+C'),
            (tr('edit_paste'), 'Ctrl+V'),
            (tr('help'), 'F1')
        ]
        
        for action, shortcut in shortcuts:
            tree.insert('', tk.END, values=(action, shortcut))
