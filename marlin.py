#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Marlin Configurator - Main Entry Point

This script serves as the main entry point for the Marlin Configurator application.
It initializes the application and starts the main event loop.
"""

import sys
import os
from pathlib import Path

def main():
    """Main entry point for the Marlin Configurator application."""
    # Add the project root to the Python path
    project_root = Path(__file__).parent
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    try:
        from app.main import MarlinConfigurator
        
        # Create and run the application
        app = MarlinConfigurator()
        
        # Set application icon if available
        try:
            icon_path = project_root / "assets" / "icon.ico"
            if icon_path.exists():
                app.iconbitmap(str(icon_path))
        except Exception as e:
            print(f"Warning: Could not set application icon: {e}")
        
        # Start the main event loop
        app.mainloop()
        
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("Please make sure all dependencies are installed.")
        print("You can install them using: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
