# Marlin Configurator API Documentation

## Table of Contents

- [Core Modules](#core-modules)
  - [Application](#application)
  - [Configuration](#configuration)
  - [Serial Communication](#serial-communication)
  - [GUI Components](#gui-components)
  - [Utilities](#utilities)
- [Extension API](#extension-api)
- [Event System](#event-system)
- [Plugin System](#plugin-system)
- [Internationalization](#internationalization)
- [Error Handling](#error-handling)
- [Logging](#logging)
- [Examples](#examples)

## Core Modules

### Application

#### `app.main`

Main application entry point.

**Classes:**
- `MainApplication`: Main application class that initializes and runs the application.

**Methods:**
- `__init__()`: Initialize the application.
- `run()`: Start the main event loop.
- `on_exit()`: Clean up resources before exit.

### Configuration

#### `config.manager`

Configuration management system.

**Classes:**
- `ConfigManager`: Manages application and user configurations.

**Methods:**
- `load(config_file: str) -> dict`: Load configuration from file.
- `save(config: dict, config_file: str)`: Save configuration to file.
- `get(section: str, key: str, default=None)`: Get a configuration value.
- `set(section: str, key: str, value)`: Set a configuration value.

### Serial Communication

#### `serial.connection`

Serial port communication with 3D printers.

**Classes:**
- `PrinterConnection`: Handles serial communication with 3D printers.

**Methods:**
- `connect(port: str, baudrate: int)`: Connect to a printer.
- `disconnect()`: Disconnect from the printer.
- `send_command(command: str)`: Send a G-code command.
- `read_response() -> str`: Read response from the printer.
- `is_connected() -> bool`: Check if connected to a printer.

## GUI Components

### Main Window

#### `gui.main_window`

Main application window.

**Classes:**
- `MainWindow`: Main application window class.

**Methods:**
- `create_menu()`: Create the main menu.
- `create_toolbar()`: Create the toolbar.
- `create_statusbar()`: Create the status bar.
- `show_about()`: Show the About dialog.
- `show_help()`: Show the Help dialog.
- `show_sponsor()`: Show the Sponsor dialog.

### Code Editor

#### `gui.code_editor`

Syntax-highlighting code editor.

**Classes:**
- `CodeEditor`: Enhanced text editor with syntax highlighting.
- `LineNumbers`: Line numbers widget.
- `SyntaxHighlighter`: Syntax highlighter for Marlin configuration.

**Methods:**
- `set_theme(theme: str)`: Set the editor theme.
- `set_font(font_family: str, size: int)`: Set the editor font.
- `load_file(file_path: str)`: Load file into the editor.
- `save_file(file_path: str)`: Save editor content to file.

## Utilities

### Internationalization

#### `lang`

Internationalization support.

**Functions:**
- `tr(key: str, **kwargs) -> str`: Translate a string.
- `set_language(lang_code: str)`: Set the current language.
- `get_available_languages() -> list`: Get list of available languages.

### Error Handling

#### `traceback`

Error handling and logging.

**Functions:**
- `log_exception(exc_type, exc_value, exc_traceback)`: Log an exception.
- `handle_uncaught_exception(exc_type, exc_value, exc_traceback)`: Handle uncaught exceptions.

**Classes:**
- `ErrorLogger`: Context manager for error handling.

## Extension API

### Plugin System

#### `plugins.base`

Base classes for plugins.

**Classes:**
- `PluginBase`: Base class for all plugins.
- `ToolPlugin`: Base class for tool plugins.
- `ViewPlugin`: Base class for view plugins.

**Methods:**
- `activate()`: Called when the plugin is activated.
- `deactivate()`: Called when the plugin is deactivated.
- `get_name() -> str`: Get the plugin name.
- `get_version() -> str`: Get the plugin version.

## Event System

### Event Handling

#### `events`

Event handling system.

**Classes:**
- `EventEmitter`: Event emitter class.
- `Event`: Base event class.

**Methods:**
- `subscribe(event_type: str, callback)`: Subscribe to an event.
- `unsubscribe(event_type: str, callback)`: Unsubscribe from an event.
- `emit(event: Event)`: Emit an event.

## Examples

### Basic Usage

```python
from app.main import MainApplication

if __name__ == "__main__":
    app = MainApplication()
    app.run()
```

### Creating a Plugin

```python
from plugins.base import ToolPlugin

class MyTool(ToolPlugin):
    def __init__(self):
        super().__init__()
        self.name = "My Tool"
        self.version = "1.0.0"
    
    def activate(self):
        print(f"{self.name} activated!")
    
    def deactivate(self):
        print(f"{self.name} deactivated!")
```

### Using the Serial Connection

```python
from serial.connection import PrinterConnection

printer = PrinterConnection()
try:
    printer.connect("/dev/ttyUSB0", 115200)
    printer.send_command("M105")
    response = printer.read_response()
    print(f"Printer response: {response}")
except Exception as e:
    print(f"Error: {e}")
finally:
    printer.disconnect()
```

## License

This documentation is part of the Marlin Configurator project and is licensed under the GPL-3.0 License.
