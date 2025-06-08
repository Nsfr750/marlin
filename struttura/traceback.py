"""
Traceback Logger 
"""

import sys
import traceback
import logging
from typing import Optional, Type, Any, Tuple, Dict
from datetime import datetime
from pathlib import Path

from .lang import tr

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('traceback.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any] = None
) -> None:
    """Log an exception with full traceback.
    
    Args:
        exc_type: The exception type
        exc_value: The exception value
        exc_traceback: The traceback object
    """
    if exc_traceback is None:
        exc_traceback = exc_value.__traceback__
    
    # Format the exception
    exc_info = (exc_type, exc_value, exc_traceback)
    
    # Log the exception
    logger.critical(
        "Unhandled exception",
        exc_info=exc_info,
        stack_info=True
    )

def handle_uncaught_exception(
    exc_type: Type[BaseException],
    exc_value: BaseException,
    exc_traceback: Optional[Any]
) -> None:
    """Handle uncaught exceptions globally.
    
    Args:
        exc_type: The exception type
        exc_value: The exception value
        exc_traceback: The traceback object
    """
    # Don't handle keyboard interrupts
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    # Log the exception
    log_exception(exc_type, exc_value, exc_traceback)
    
    # Show error to user (if possible)
    try:
        import tkinter as tk
        from tkinter import messagebox
        
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        error_msg = f"{tr('unexpected_error')}:\n{str(exc_value)}"
        messagebox.showerror(
            tr('error'),
            f"{error_msg}\n\n{tr('error_logged')}"
        )
        root.destroy()
    except Exception as e:
        # If we can't show a GUI error, log it
        logger.error("Failed to show error dialog: %s", str(e))
    
    # Call the default exception handler
    sys.__excepthook__(exc_type, exc_value, exc_traceback)

class ErrorLogger:
    """Context manager for logging exceptions."""
    
    def __init__(self, logger_name: str = None):
        """Initialize the error logger.
        
        Args:
            logger_name: The name of the logger to use
        """
        self.logger = logging.getLogger(logger_name or __name__)
    
    def __enter__(self):
        """Enter the context."""
        return self
    
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[Any]
    ) -> bool:
        """Exit the context, logging any exceptions.
        
        Args:
            exc_type: The exception type
            exc_value: The exception value
            exc_traceback: The traceback object
            
        Returns:
            bool: True if the exception was handled
        """
        if exc_type is not None:
            self.logger.error(
                "Exception in context",
                exc_info=(exc_type, exc_value, exc_traceback)
            )
        return True  # Suppress the exception

def setup_global_exception_handler() -> None:
    """Set up the global exception handler."""
    sys.excepthook = handle_uncaught_exception

def log_info(message: str, **kwargs: Any) -> None:
    """Log an info message.
    
    Args:
        message: The message to log
        **kwargs: Additional context
    """
    logger.info(message, extra=kwargs)

def log_warning(message: str, **kwargs: Any) -> None:
    """Log a warning message.
    
    Args:
        message: The message to log
        **kwargs: Additional context
    """
    logger.warning(message, extra=kwargs)

def log_error(message: str, **kwargs: Any) -> None:
    """Log an error message.
    
    Args:
        message: The message to log
        **kwargs: Additional context
    """
    logger.error(message, extra=kwargs)

def log_critical(message: str, **kwargs: Any) -> None:
    """Log a critical message.
    
    Args:
        message: The message to log
        **kwargs: Additional context
    """
    logger.critical(message, extra=kwargs)

# Set up global exception handler when module is imported
setup_global_exception_handler()
