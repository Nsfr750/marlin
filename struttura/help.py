"""
Help Dialog Module

This module provides the Help dialog for Marlin Configurator.
Displays usage instructions, features, and keyboard shortcuts in a tabbed interface.

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
        help_dialog.geometry('900x700')
        help_dialog.minsize(700, 500)
        help_dialog.transient(parent)
        help_dialog.grab_set()
        
        # Center the dialog on the parent window
        window_width = 900
        window_height = 700
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
            'quick_start': tr('quick_start'),
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
        Help._setup_quick_start_tab(tab_frames['quick_start'])
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
    def _setup_quick_start_tab(parent: ttk.Frame) -> None:
        """Set up the Quick Start tab content."""
        text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=('Helvetica', 10),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True)
        
        quick_start_text = """Marlin Configurator - Quick Start Guide

1. Connecting to Your Printer:
   - Select the correct serial port from the dropdown
   - Choose the appropriate baud rate (usually 115200 or 250000)
   - Click 'Connect' to establish a connection

2. Loading Configuration:
   - Go to File > Open to load a configuration file
   - Or connect to your printer to fetch current settings

3. Editing Settings:
   - Navigate through the configuration tabs
   - Modify settings as needed
   - Changes are automatically validated

4. Saving and Uploading:
   - Save your configuration with File > Save
   - Upload to your printer using the 'Upload' button

For more detailed information, see the other tabs.
"""
        text.insert(tk.END, quick_start_text)
        text.config(state=tk.DISABLED)
    
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
        
        usage_text = """Marlin Configurator - Usage Guide

Configuration Management:
- Open existing configuration files in INI format
- Save your configuration to a file
- Compare different configurations
- Validate settings before uploading

Printer Connection:
- Connect to your 3D printer via USB
- Read current configuration
- Upload new settings directly to the printer
- Monitor printer status

Editor Features:
- Syntax highlighting for configuration files
- Line numbers and code folding
- Search and replace functionality
- Keyboard shortcuts for common actions

For a complete list of features, see the Features tab.
"""
        text.insert(tk.END, usage_text)
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
        
        features_text = """Marlin Configurator - Features

Core Features:
- Intuitive graphical interface
- Support for all Marlin firmware versions
- Real-time configuration validation
- Printer connection management
- Configuration backup and restore

Advanced Features:
- Multiple configuration profiles
- Configuration comparison tool
- Direct printer firmware upload
- Comprehensive error checking
- Customizable interface

Supported Printers:
- All Marlin-based 3D printers
- Cartesian, Delta, and CoreXY configurations
- Single and multi-extruder setups
- Support for various bed leveling systems
"""
        text.insert(tk.END, features_text)
        text.config(state=tk.DISABLED)
    
    @staticmethod
    def _setup_shortcuts_tab(parent: ttk.Frame) -> None:
        """Set up the Keyboard Shortcuts tab content."""
        text = scrolledtext.ScrolledText(
            parent,
            wrap=tk.WORD,
            font=('Courier', 10),
            padx=10,
            pady=10
        )
        text.pack(fill=tk.BOTH, expand=True)
        
        shortcuts = """Keyboard Shortcuts

File Operations:
Ctrl+O       Open configuration file
Ctrl+S       Save current configuration
Ctrl+Shift+S Save configuration as...
Ctrl+Q       Exit application

Edit Operations:
Ctrl+Z       Undo last action
Ctrl+Y       Redo last action
Ctrl+X       Cut selected text
Ctrl+C       Copy selected text
Ctrl+V       Paste text
Ctrl+A       Select all text

View Operations:
F11          Toggle fullscreen
Ctrl++       Zoom in
Ctrl+-       Zoom out
Ctrl+0       Reset zoom

Navigation:
Ctrl+F       Find in document
F3           Find next
Shift+F3     Find previous
Ctrl+G       Go to line
"""
        text.insert(tk.END, shortcuts)
        text.config(state=tk.DISABLED)
