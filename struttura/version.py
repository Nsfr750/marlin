"""Version information for the application.

This module follows Semantic Versioning 2.0.0 (https://semver.org/).
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional, Tuple
import re
import sys
from datetime import datetime

from .lang import tr

# Version information
__version__ = "1.0.0"
__version_info__ = (1, 0, 0)
__build__ = ""
__author__ = "Nsfr750"
__email__ = "nsfr750@yandex.com"
__license__ = "GPL-3.0"
__copyright__ = f" 2025 {__author__}"

# Project information
PROJECT_NAME = "Marlin Configurator"
PROJECT_DESCRIPTION = "A modern GUI application for configuring Marlin firmware"
PROJECT_URL = "https://github.com/Nsfr750/marlin-configurator"

# Version suffixes for pre-release and build metadata
PRERELEASE_SUFFIX = ""  # e.g., "alpha.1", "beta.2", "rc.3"
BUILD_METADATA = ""     # e.g., "20230608"

def get_version() -> str:
    """Get the full version string.
    
    Returns:
        str: The full version string (e.g., "1.0.0" or "1.0.0-alpha.1+20230608")
    """
    version = __version__
    if PRERELEASE_SUFFIX:
        version += f"-{PRERELEASE_SUFFIX}"
    if BUILD_METADATA:
        version += f"+{BUILD_METADATA}"
    return version

def get_version_info() -> Dict[str, Any]:
    """Get detailed version information.
    
    Returns:
        dict: A dictionary containing version information
    """
    return {
        'version': __version__,
        'version_info': __version_info__,
        'prerelease': PRERELEASE_SUFFIX,
        'build': BUILD_METADATA or None,
        'full_version': get_version(),
        'author': __author__,
        'email': __email__,
        'license': __license__,
        'copyright': __copyright__,
        'project': PROJECT_NAME,
        'description': PROJECT_DESCRIPTION,
        'url': PROJECT_URL,
        'python': sys.version.split(' ')[0],
        'build_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

def show_version(parent: Optional[tk.Tk] = None) -> None:
    """Show version information in a dialog.
    
    Args:
        parent: The parent window
    """
    version_info = get_version_info()
    
    # Create dialog
    dialog = tk.Toplevel(parent) if parent else tk.Tk()
    dialog.title(f"{tr('about')} {version_info['project']}")
    dialog.resizable(False, False)
    
    if parent:
        dialog.transient(parent)
        dialog.grab_set()
    else:
        dialog.withdraw()  # Hide root window if no parent
    
    # Center the dialog
    dialog.update_idletasks()
    width = 400
    height = 400
    x = (dialog.winfo_screenwidth() // 2) - (width // 2)
    y = (dialog.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    # Main container
    container = ttk.Frame(dialog, padding="20")
    container.pack(fill=tk.BOTH, expand=True)
    
    # Application title
    title_label = ttk.Label(
        container,
        text=version_info['project'],
        font=('Helvetica', 16, 'bold')
    )
    title_label.pack(pady=(0, 10))
    
    # Version
    version_text = f"{tr('version')} {version_info['full_version']}"
    if version_info['prerelease']:
        version_text += f" ({version_info['prerelease']})"
    
    version_label = ttk.Label(
        container,
        text=version_text,
        font=('Helvetica', 10)
    )
    version_label.pack(pady=(0, 20))
    
    # Info frame
    info_frame = ttk.LabelFrame(
        container,
        text=tr('system_info'),
        padding=10
    )
    info_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
    
    # System information
    rows = [
        (tr('python_version'), version_info['python']),
        (tr('build_date'), version_info['build_date']),
        (tr('license'), version_info['license']),
        (tr('author'), version_info['author']),
        (tr('email'), version_info['email'])
    ]
    
    for i, (label, value) in enumerate(rows):
        # Label
        ttk.Label(
            info_frame,
            text=f"{label}:",
            font=('Helvetica', 9, 'bold')
        ).grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
        
        # Value
        ttk.Label(
            info_frame,
            text=value,
            font=('Helvetica', 9)
        ).grid(row=i, column=1, sticky=tk.W, pady=2, padx=5)
    
    # Copyright
    copyright_label = ttk.Label(
        container,
        text=version_info['copyright'],
        font=('Helvetica', 8)
    )
    copyright_label.pack(side=tk.BOTTOM, pady=(10, 0))
    
    # Close button
    close_btn = ttk.Button(
        container,
        text=tr('close'),
        command=dialog.destroy
    )
    close_btn.pack(side=tk.BOTTOM, pady=(10, 0))
    
    # Make dialog modal
    if parent:
        dialog.wait_window(dialog)
    else:
        dialog.deiconify()  # Show the dialog if it was hidden
        dialog.mainloop()

def check_version(current_version: str, latest_version: str) -> Tuple[bool, str]:
    """Check if a newer version is available.
    
    Args:
        current_version: The current version string
        latest_version: The latest version string to compare against
        
    Returns:
        tuple: (is_update_available, message)
    """
    def parse_version(version: str) -> Tuple[Tuple[int, ...], str, str]:
        # Parse version string into (version_parts, prerelease, build)
        version = version.strip()
        build = ""
        prerelease = ""
        
        # Extract build metadata
        if '+' in version:
            version, build = version.split('+', 1)
        
        # Extract prerelease
        if '-' in version:
            version, prerelease = version.split('-', 1)
        
        # Parse version numbers
        try:
            version_parts = tuple(map(int, version.split('.')))
        except ValueError:
            version_parts = (0, 0, 0)
        
        return version_parts, prerelease, build
    
    try:
        current_parts, current_prerelease, _ = parse_version(current_version)
        latest_parts, latest_prerelease, _ = parse_version(latest_version)
        
        # Compare version parts
        if latest_parts > current_parts:
            return True, tr('update_available').format(version=latest_version)
        
        # If versions are the same, compare prerelease
        if latest_parts == current_parts and latest_prerelease and not current_prerelease:
            return True, tr('prerelease_available').format(version=latest_version)
        
        return False, tr('latest_version_installed')
    except Exception as e:
        return False, tr('version_check_failed').format(error=str(e))
