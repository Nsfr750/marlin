import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml
import serial.tools.list_ports
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.code_editor import CodeEditor
from struttura.menu import create_menu_bar
from struttura.lang import tr, set_language
from struttura.traceback import log_exception

class MarlinConfigurator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(tr('app_title'))
        self.geometry("1200x800")
        self.minsize(1000, 700)
        
        # Set up exception handling
        sys.excepthook = self.handle_exception
        
        # Variables
        self.port_var = tk.StringVar()
        self.baudrate_var = tk.StringVar(value="115200")
        self.config_path = tk.StringVar()
        self.connected = False
        self.current_file = None
        self.modified = False
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Create menu bar
        self.menu_bar = create_menu_bar(self, self)
        
        # Setup UI
        self.setup_ui()
        self.update_ports()
        
        # Bind keyboard shortcuts
        self.bind('<Control-o>', lambda e: self.load_config())
        self.bind('<Control-s>', lambda e: self.save_config())
        self.bind('<Control-S>', lambda e: self.save_as_config())
    
    def setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self, padding="5")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Connection frame
        conn_frame = ttk.LabelFrame(main_frame, text="Printer Connection", padding="5")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Port selection
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.port_combobox = ttk.Combobox(conn_frame, textvariable=self.port_var, width=20)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Refresh ports button
        ttk.Button(
            conn_frame, 
            text="Refresh", 
            command=self.update_ports
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Baud rate selection
        ttk.Label(conn_frame, text="Baudrate:").grid(row=0, column=3, padx=5, pady=5, sticky='e')
        baudrates = ["9600", "19200", "38400", "57600", "115200", "230400", "250000"]
        baudrate_combobox = ttk.Combobox(
            conn_frame, 
            textvariable=self.baudrate_var, 
            values=baudrates,
            width=10
        )
        baudrate_combobox.grid(row=0, column=4, padx=5, pady=5, sticky='w')
        
        # Connect/Disconnect button
        self.connect_btn = ttk.Button(
            conn_frame, 
            text="Connect", 
            command=self.toggle_connection,
            width=10
        )
        self.connect_btn.grid(row=0, column=5, padx=5, pady=5)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Editor tab
        self.setup_editor_tab()
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set(tr('ready_status'))
        status_bar = ttk.Label(
            self, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_editor_tab(self):
        """Set up the editor tab with the code editor"""
        self.editor_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.editor_tab, text="Editor")
        
        # Create editor
        self.editor = CodeEditor(self.editor_tab)
        self.editor.pack(fill=tk.BOTH, expand=True)
    
    def update_ports(self):
        """Update the list of available serial ports"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combobox['values'] = ports
        if ports:
            self.port_combobox.set(ports[0])
    
    def toggle_connection(self):
        """Toggle connection to the printer"""
        if not self.connected:
            self.connect_printer()
        else:
            self.disconnect_printer()
    
    def connect_printer(self):
        """Connect to the printer"""
        port = self.port_var.get()
        baudrate = self.baudrate_var.get()
        
        if not port:
            messagebox.showerror("Error", "Please select a port")
            return
        
        try:
            # Here you would implement the actual connection logic
            # For now, we'll just simulate a successful connection
            self.connected = True
            self.connect_btn.configure(text="Disconnect")
            self.status_var.set(f"Connected to {port} @ {baudrate} baud")
            messagebox.showinfo("Success", f"Connected to {port}")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
    
    def disconnect_printer(self):
        """Disconnect from the printer"""
        self.connected = False
        self.connect_btn.configure(text="Connect")
        self.status_var.set("Disconnected")
    
    def load_config(self, event=None):
        """Load configuration from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("YAML files", "*.yaml;*.yml"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r') as f:
                config_data = yaml.safe_load(f)
                self.editor.delete('1.0', tk.END)
                self.editor.insert(tk.END, yaml.dump(config_data, default_flow_style=False))
                self.current_file = file_path
                self.status_var.set(f"Loaded {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file: {str(e)}")
    
    def save_config(self, event=None):
        """Save configuration to the current file"""
        if not self.current_file:
            self.save_as_config()
            return
        
        try:
            config_data = yaml.safe_load(self.editor.get('1.0', tk.END))
            with open(self.current_file, 'w') as f:
                yaml.dump(config_data, f, default_flow_style=False)
            self.status_var.set(f"Saved {os.path.basename(self.current_file)}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")
    
    def save_as_config(self, event=None):
        """Save configuration to a new file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.current_file = file_path
        self.save_config()
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        log_exception(exc_type, exc_value, exc_traceback)
        
        # Show error to user
        error_msg = f"An unexpected error occurred: {str(exc_value)}"
        self.status_var.set(tr('error', msg=error_msg))
        
        # Show error dialog
        messagebox.showerror(
            "Error",
            f"An unexpected error occurred:\n{str(exc_value)}\n\n"
            "The error has been logged. Please contact support if the problem persists."
        )
    
    # Editor commands
    def undo(self):
        try:
            self.editor.edit_undo()
        except:
            pass
    
    def redo(self):
        try:
            self.editor.edit_redo()
        except:
            pass
    
    def cut(self):
        self.editor.event_generate("<<Cut>>")
    
    def copy(self):
        self.editor.event_generate("<<Copy>>")
    
    def paste(self):
        self.editor.event_generate("<<Paste>>")

def main():
    app = MarlinConfigurator()
    app.mainloop()

if __name__ == "__main__":
    main()
