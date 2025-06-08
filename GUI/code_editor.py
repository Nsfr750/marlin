import tkinter as tk
from tkinter import ttk, font as tkfont
from pygments import lex
from pygments.lexers import CppLexer, get_lexer_by_name
from pygments.token import Token

class LineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, **kwargs):
        # Set default values
        kwargs.setdefault('width', 40)
        kwargs.setdefault('bg', '#f0f0f0')
        kwargs.setdefault('bd', 0)
        kwargs.setdefault('highlightthickness', 0)
        
        super().__init__(master, **kwargs)
        
        # Store the text widget reference
        self.text_widget = text_widget
        
        # Configure font
        self.font_family = 'Consolas'
        self.font_size = 10
        
        # Check if Consolas is available, otherwise use a fallback
        available_fonts = list(tkfont.families())
        if 'Consolas' not in available_fonts:
            # Try common monospace fonts in order of preference
            for font in ['DejaVu Sans Mono', 'Liberation Mono', 'Courier New', 'Courier', 'monospace']:
                if font in available_fonts:
                    self.font_family = font
                    break
        
        self.font = tkfont.Font(family=self.font_family, size=self.font_size)
        
        # Configure the text widget's font if it exists
        if self.text_widget:
            self.text_widget.config(font=self.font)
        
        # Bind events if we have a text widget
        if self.text_widget:
            self.text_widget.bind('<KeyRelease>', self.on_key_release)
            self.text_widget.bind('<Button-1>', self.on_click)
            self.text_widget.bind('<MouseWheel>', self.on_mousewheel)
        
        self.bind('<Configure>', self.on_configure)
        
        # Initial update
        self.update_line_numbers()
    
    def on_key_release(self, event=None):
        self.update_line_numbers()
    
    def on_click(self, event=None):
        self.update_line_numbers()
    
    def on_mousewheel(self, event):
        self.update_line_numbers()
    
    def on_configure(self, event=None):
        self.update_line_numbers()
    
    def update_line_numbers(self):
        """Update the line numbers"""
        self.delete("all")
        
        # Get the number of lines in the text widget
        lines = self.text_widget.get("1.0", "end-1c").split("\n")
        num_lines = len(lines)
        
        # Set the width of the line numbers column
        width = self.font.measure(str(num_lines) + ' ')
        self.config(width=width + 10)  # Add some padding
        
        # Draw line numbers
        for i in range(num_lines):
            self.create_text(
                width - 5,  # Right-align the numbers
                (i + 1) * self.font.metrics("linespace") - 2,  # Vertical position
                text=str(i + 1),
                font=self.font,
                anchor="ne",
                fill="#666666"
            )


class CodeEditor(ttk.Frame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create text widget first
        self.text = tk.Text(
            self, 
            wrap=tk.WORD, 
            undo=True, 
            autoseparators=True,
            maxundo=-1,
            font=('Consolas', 10),
            padx=5,
            pady=5,
            bd=0,
            highlightthickness=0
        )
        
        # Now create line numbers with reference to the text widget
        self.line_numbers = LineNumbers(self, self.text)
        self.line_numbers.grid(row=0, column=0, sticky='ns')
        
        # Place the text widget
        self.text.grid(row=0, column=1, sticky='nsew')
        
        # Configure tags for syntax highlighting
        self.configure_tags()
        
        # Bind events
        self.text.bind('<KeyRelease>', self.on_key_release)
        self.text.bind('<Key>', self.on_key_press)
        
        # Configure scrollbar
        self.scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.text.yview)
        self.scrollbar.grid(row=0, column=2, sticky='ns')
        self.text.config(yscrollcommand=self.scrollbar.set)
        
        # Context menu
        self.setup_context_menu()
        
        # Initialize lexer for syntax highlighting
        self.lexer = CppLexer()
        
        # Schedule initial syntax highlighting
        self.after(100, self.highlight_syntax)
    
    def configure_tags(self):
        """Configure text tags for syntax highlighting"""
        # Default text style
        self.text.tag_configure('default', foreground='#000000')
        
        # Syntax highlighting styles
        self.text.tag_configure('Token.Keyword', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Constant', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Declaration', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Namespace', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Pseudo', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Reserved', foreground='#0000FF')
        self.text.tag_configure('Token.Keyword.Type', foreground='#2B91AF')
        self.text.tag_configure('Token.Name.Class', foreground='#2B91AF')
        self.text.tag_configure('Token.Name.Function', foreground='#795E26')
        self.text.tag_configure('Token.String', foreground='#A31515')
        self.text.tag_configure('Token.Comment', foreground='#008000')
        self.text.tag_configure('Token.Comment.Multiline', foreground='#008000')
        self.text.tag_configure('Token.Number', foreground='#098658')
        self.text.tag_configure('Token.Operator', foreground='#000000')
    
    def setup_context_menu(self):
        """Set up the right-click context menu"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut)
        self.context_menu.add_command(label="Copy", command=self.copy)
        self.context_menu.add_command(label="Paste", command=self.paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all)
        
        # Bind right-click event
        self.text.bind("<Button-3>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Show the context menu on right-click"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def on_key_press(self, event):
        """Handle key press events"""
        # Auto-indent on Enter
        if event.keysym == 'Return':
            self.auto_indent()
            return 'break'
        # Auto-close brackets and quotes
        elif event.char in '\"\'\`(){}[]':
            self.auto_close_bracket(event.char)
            return 'break'
        # Tab key handling
        elif event.keysym == 'Tab':
            self.text.insert(tk.INSERT, '    ')
            return 'break'
    
    def on_key_release(self, event):
        """Handle key release events"""
        self.highlight_syntax()
    
    def auto_indent(self):
        """Auto-indent the current line based on the previous line"""
        current_line = self.text.index(tk.INSERT).split('.')[0]
        previous_line = str(int(current_line) - 1)
        
        # Get the indentation of the previous line
        previous_text = self.text.get(f"{previous_line}.0", f"{previous_line}.end")
        indent = len(previous_text) - len(previous_text.lstrip())
        
        # Insert newline and the same indentation
        self.text.insert(tk.INSERT, '\n' + ' ' * indent)
    
    def auto_close_bracket(self, char):
        """Auto-close brackets, quotes, etc."""
        pairs = {
            '"': '"',
            "'": "'",
            '`': '`',
            '(': ')',
            '[': ']',
            '{': '}'
        }
        
        if char in pairs:
            self.text.insert(tk.INSERT, char + pairs[char])
            self.text.mark_set(tk.INSERT, f"insert -1c")
    
    def highlight_syntax(self):
        """Apply syntax highlighting to the entire document"""
        try:
            # Get the text content
            content = self.text.get("1.0", tk.END)
            if not content.strip():
                return
            
            # Remove all existing tags
            for tag in self.text.tag_names():
                if tag != 'sel':
                    self.text.tag_remove(tag, "1.0", tk.END)
            
            # Tokenize the content
            tokens = lex(content, self.lexer)
            
            # Apply highlighting
            for token_type, value in tokens:
                if token_type in Token.Text or not value.strip():
                    continue
                
                # Get the tag name from the token type
                tag_name = str(token_type)
                
                # Apply the tag to each occurrence of the value
                start = "1.0"
                while True:
                    start = self.text.search(value, start, stopindex=tk.END, regexp=True)
                    if not start:
                        break
                    end = f"{start}+{len(value)}c"
                    self.text.tag_add(tag_name, start, end)
                    start = end
                    
        except Exception as e:
            # Ignore highlighting errors
            pass
    
    # Standard text widget methods
    def get(self, index1, index2=None):
        return self.text.get(index1, index2)
    
    def insert(self, index, text, tags=None):
        if tags:
            self.text.insert(index, text, tags)
        else:
            self.text.insert(index, text)
    
    def delete(self, index1, index2=None):
        self.text.delete(index1, index2)
    
    def edit_undo(self):
        try:
            self.text.edit_undo()
        except:
            pass
    
    def edit_redo(self):
        try:
            self.text.edit_redo()
        except:
            pass
    
    def cut(self):
        self.event_generate("<<Cut>>")
    
    def copy(self):
        self.event_generate("<<Copy>>")
    
    def paste(self):
        self.event_generate("<<Paste>>")
    
    def select_all(self):
        self.text.tag_add(tk.SEL, "1.0", tk.END)
        self.text.mark_set(tk.INSERT, "1.0")
        self.text.see(tk.INSERT)
        return 'break'
