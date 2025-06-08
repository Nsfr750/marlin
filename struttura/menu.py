import tkinter as tk
from tkinter import messagebox
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any, Callable

from .about import About
from .help import Help
from .sponsor import Sponsor
from .log_viewer import LogViewer
from .version import show_version
from .lang import tr, set_language, get_available_languages

def create_menu_bar(root, app) -> tk.Menu:
    """
    Create and return the main menu bar with all menus and commands.
    
    Args:
        root: The root window
        app: The main application instance (MarlinConfigurator)
        
    Returns:
        tk.Menu: The configured menu bar
    """
    menubar = tk.Menu(root)
    root.config(menu=menubar)

    # File menu
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(
        label=tr('open'),
        command=app.load_config,
        accelerator="Ctrl+O"
    )
    file_menu.add_separator()
    file_menu.add_command(
        label=tr('save'),
        command=app.save_config,
        accelerator="Ctrl+S"
    )
    file_menu.add_command(
        label=tr('save_as'),
        command=app.save_as_config,
        accelerator="Ctrl+Shift+S"
    )
    file_menu.add_separator()
    file_menu.add_command(
        label=tr('exit'),
        command=root.quit,
        accelerator="Alt+F4"
    )
    menubar.add_cascade(label=tr('file'), menu=file_menu)

    # Edit menu
    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(
        label=tr('undo'),
        command=app.undo,
        accelerator="Ctrl+Z"
    )
    edit_menu.add_command(
        label=tr('redo'),
        command=app.redo,
        accelerator="Ctrl+Y"
    )
    edit_menu.add_separator()
    edit_menu.add_command(
        label=tr('cut'),
        command=app.cut,
        accelerator="Ctrl+X"
    )
    edit_menu.add_command(
        label=tr('copy'),
        command=app.copy,
        accelerator="Ctrl+C"
    )
    edit_menu.add_command(
        label=tr('paste'),
        command=app.paste,
        accelerator="Ctrl+V"
    )
    menubar.add_cascade(label=tr('edit'), menu=edit_menu)

    # View menu
    view_menu = tk.Menu(menubar, tearoff=0)
    if hasattr(app, 'toggle_line_numbers'):
        view_menu.add_checkbutton(
            label=tr('line_numbers'),
            command=app.toggle_line_numbers
        )
    menubar.add_cascade(label=tr('view'), menu=view_menu)

    # Connection menu
    if hasattr(app, 'toggle_connection'):
        connection_menu = tk.Menu(menubar, tearoff=0)
        connection_menu.add_command(
            label=tr('connect'),
            command=app.toggle_connection
        )
        if hasattr(app, 'update_ports'):
            connection_menu.add_command(
                label=tr('refresh_ports'),
                command=app.update_ports
            )
        menubar.add_cascade(label=tr('connection'), menu=connection_menu)

    # Log menu
    log_menu = tk.Menu(menubar, tearoff=0)
    log_menu.add_command(
        label=tr('view_log'),
        command=lambda: LogViewer.show_log(root)
    )
    menubar.add_cascade(label=tr('log'), menu=log_menu)

    # Help menu
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(
        label=tr('help'),
        command=lambda: Help.show_help(root)
    )
    help_menu.add_separator()
    help_menu.add_command(
        label=tr('about'),
        command=lambda: About.show_about(root)
    )
    help_menu.add_command(
        label=tr('sponsor'),
        command=lambda: Sponsor(root).show_sponsor()
    )
    menubar.add_cascade(label=tr('help'), menu=help_menu)

    # Language menu
    def set_lang_and_restart(lang_code: str) -> None:
        """Set the application language and restart if needed."""
        if set_language(lang_code):
            if messagebox.askyesno(
                tr('restart_required'),
                tr('restart_confirmation')
            ):
                root.destroy()
                os.execl(sys.executable, sys.executable, *sys.argv)

    lang_menu = tk.Menu(menubar, tearoff=0)
    for code, name in get_available_languages().items():
        lang_menu.add_command(
            label=name,
            command=lambda c=code: set_lang_and_restart(c)
        )
    menubar.add_cascade(label=tr('language'), menu=lang_menu)

    # Version info (right-aligned)
    if hasattr(app, 'version_var'):
        version_menu = tk.Menu(menubar, tearoff=0)
        version_menu.add_command(
            label=tr('version_info'),
            command=lambda: show_version(root)
        )
        menubar.add_cascade(label=tr('version'), menu=version_menu)

    return menubar
