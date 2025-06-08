import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import yaml
import serial.tools.list_ports
from GUI.code_editor import CodeEditor
from struttura.menu import create_menu_bar
from struttura.lang import tr, set_language
from struttura.traceback import log_exception
import sys
import os

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
        conn_frame = ttk.LabelFrame(main_frame, text=tr('connection'), padding="5")
        conn_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Port selection
        ttk.Label(conn_frame, text=f"{tr('port')}:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.port_combobox = ttk.Combobox(conn_frame, textvariable=self.port_var, width=20)
        self.port_combobox.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        
        # Refresh ports button
        ttk.Button(
            conn_frame, 
            text=tr('refresh'), 
            command=self.update_ports
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Baud rate selection
        ttk.Label(conn_frame, text=f"{tr('baudrate')}:").grid(row=0, column=3, padx=5, pady=5, sticky='e')
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
            text=tr('connect'), 
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
        self.notebook.add(self.editor_tab, text=tr('editor'))
        
        # Create editor
        self.editor = CodeEditor(self.editor_tab)
        self.editor.pack(fill=tk.BOTH, expand=True)
    
    def update_ports(self):
        """Update the list of available serial ports"""
        try:
            ports = [port.device for port in serial.tools.list_ports.comports()]
            self.port_combobox['values'] = ports
            if ports:
                self.port_combobox.set(ports[0])
            self.status_var.set(tr('ports_updated'))
        except Exception as e:
            self.status_var.set(tr('error_ports'))
    
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
            messagebox.showerror(tr('error'), tr('select_port'))
            return
        
        try:
            # Here you would implement the actual connection logic
            # For now, we'll just simulate a successful connection
            self.connected = True
            self.connect_btn.configure(text=tr('disconnect'))
            self.status_var.set(tr('connected').format(port=port, baudrate=baudrate))
            messagebox.showinfo(tr('success'), tr('connected_to').format(port=port))
        except Exception as e:
            messagebox.showerror(tr('connection_error'), f"{tr('connection_failed')}: {str(e)}")
    
    def disconnect_printer(self):
        """Disconnect from the printer"""
        self.connected = False
        self.connect_btn.configure(text=tr('connect'))
        self.status_var.set(tr('disconnected'))
    
    def load_config(self, event=None):
        """Load configuration from a file"""
        file_path = filedialog.askopenfilename(
            filetypes=[("YAML files", "*.yaml;*.yml"), ("All files", "*.*")],
            title=tr('open_config')
        )
        
        if not file_path:
            return
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = yaml.safe_load(f)
                self.editor.delete('1.0', tk.END)
                self.editor.insert(tk.END, yaml.dump(config_data, default_flow_style=False, allow_unicode=True))
                self.current_file = file_path
                self.status_var.set(tr('file_loaded').format(file=os.path.basename(file_path)))
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('load_error')}: {str(e)}")
    
    def save_config(self, event=None):
        """Save configuration to the current file"""
        if not self.current_file:
            self.save_as_config()
            return
        
        try:
            config_data = yaml.safe_load(self.editor.get('1.0', tk.END))
            with open(self.current_file, 'w', encoding='utf-8') as f:
                yaml.dump(config_data, f, default_flow_style=False, allow_unicode=True)
            self.status_var.set(tr('file_saved').format(file=os.path.basename(self.current_file)))
        except Exception as e:
            messagebox.showerror(tr('error'), f"{tr('save_error')}: {str(e)}")
    
    def save_as_config(self, event=None):
        """Save configuration to a new file"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".yaml",
            filetypes=[("YAML files", "*.yaml"), ("All files", "*.*")],
            title=tr('save_config_as')
        )
        
        if not file_path:
            return
        
        self.current_file = file_path
        self.save_config()
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        log_exception(exc_type, exc_value, exc_traceback)
        
        # Show error to user
        error_msg = f"{tr('unexpected_error')}: {str(exc_value)}"
        self.status_var.set(tr('error', msg=error_msg))
        
        # Show error dialog
        messagebox.showerror(
            tr('error'),
            f"{tr('unexpected_error')}:\n{str(exc_value)}\n\n{tr('error_logged')}"
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
