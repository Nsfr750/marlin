import tkinter as tk
from tkinter import ttk, font as tkfont
from pygments import lex
from pygments.lexers import CppLexer, get_lexer_by_name
from pygments.token import Token

class LineNumbers(tk.Canvas):
    def __init__(self, master, text_widget, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.text_widget = text_widget
        
        # Try to get a monospace font, fall back to system default if needed
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
        self.text_widget.configure(font=self.font)
        
        self.text_widget.bind('<Configure>', self._on_configure)
        self.text_widget.bind('<KeyRelease>', self._on_key_release)
        self.text_widget.bind('<MouseWheel>', self._on_mousewheel)
        self.text_widget.bind("<Button-4>", self._on_mousewheel)
        self.text_widget.bind("<Button-5>", self._on_mousewheel)
    
    def _on_configure(self, event=None):
        self.redraw()
    
    def _on_key_release(self, event=None):
        self.redraw()
    
    def _on_mousewheel(self, event):
        self.redraw()
    
    def redraw(self, *args):
        self.delete('all')
        
        # Get the visible lines
        first_visible_line = int(self.text_widget.index('@0,0').split('.')[0])
        last_visible_line = int(self.text_widget.index(f'@0,{self.text_widget.winfo_height()}').split('.')[0])
        
        # Draw line numbers
        for line in range(first_visible_line, last_visible_line + 2):
            y = self.text_widget.bbox(f'{line}.0')[1] if self.text_widget.get(f'{line}.0', f'{line}.0 lineend').strip() else -1000
            if y > 0:
                self.create_text(2, y, anchor='nw', text=str(line), font=self.font, fill="#666666")
        
        # Update scroll region
        self.configure(scrollregion=self.bbox('all'))

class CodeEditor(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.master = master
        self.setup_ui()
        
        # Configure tags for syntax highlighting
        self.setup_highlighting()
        
        # Bind events
        self.text.bind('<KeyRelease>', self._on_key_release)
        self.text.bind('<FocusIn>', self._on_focus_in)
        self.text.bind('<FocusOut>', self._on_focus_out)
        
        # Setup lexer for syntax highlighting
        self.lexer = CppLexer()
        
    def setup_ui(self):
        # Create main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create text widget with scrollbars
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Vertical scrollbar
        self.v_scrollbar = ttk.Scrollbar(self.text_frame)
        self.v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Horizontal scrollbar
        self.h_scrollbar = ttk.Scrollbar(self.text_frame, orient=tk.HORIZONTAL)
        self.h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Text widget
        self.text = tk.Text(
            self.text_frame,
            wrap=tk.NONE,
            yscrollcommand=self.v_scrollbar.set,
            xscrollcommand=self.h_scrollbar.set,
            font=('Courier New', 10),  # Default font that's widely available
            tabs=(4 * 8),  # 4 spaces for tab
            insertwidth=2,
            undo=True,
            autoseparators=True,
            maxundo=-1
        )
        self.text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure scrollbars
        self.v_scrollbar.config(command=self.text.yview)
        self.h_scrollbar.config(command=self.text.xview)
        
        # Line numbers
        self.line_numbers = LineNumbers(self.main_frame, self.text, width=50, bg='#f0f0f0', bd=0, highlightthickness=0)
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        
        # Right-click menu
        self.setup_context_menu()
    
    def setup_highlighting(self):
        # Syntax highlighting colors
        self.text.tag_configure('Token.Comment', foreground='#6A9955')
        self.text.tag_configure('Token.Keyword', foreground='#569CD6')
        self.text.tag_configure('Token.Keyword.Constant', foreground='#9CDCFE')
        self.text.tag_configure('Token.Keyword.Declaration', foreground='#C586C0')
        self.text.tag_configure('Token.Keyword.Namespace', foreground='#569CD6')
        self.text.tag_configure('Token.Keyword.Pseudo', foreground='#569CD6')
        self.text.tag_configure('Token.Keyword.Reserved', foreground='#569CD6')
        self.text.tag_configure('Token.Keyword.Type', foreground='#4EC9B0')
        self.text.tag_configure('Token.Name.Class', foreground='#4EC9B0')
        self.text.tag_configure('Token.Name.Function', foreground='#DCDCAA')
        self.text.tag_configure('Token.Name.Variable', foreground='#9CDCFE')
        self.text.tag_configure('Token.Literal.Number', foreground='#B5CEA8')
        self.text.tag_configure('Token.Literal.String', foreground='#CE9178')
        self.text.tag_configure('Token.Operator', foreground='#D4D4D4')
        self.text.tag_configure('Token.Punctuation', foreground='#D4D4D4')
        self.text.tag_configure('Token.Text', foreground='#D4D4D4')
    
    def setup_context_menu(self):
        self.context_menu = tk.Menu(self.text, tearoff=0)
        self.context_menu.add_command(label="Cut", command=self.cut)
        self.context_menu.add_command(label="Copy", command=self.copy)
        self.context_menu.add_command(label="Paste", command=self.paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all)
        
        # Bind right-click
        self.text.bind('<Button-3>', self.show_context_menu)
    
    def show_context_menu(self, event):
        self.context_menu.tk_popup(event.x_root, event.y_root)
    
    def cut(self):
        self.text.event_generate('<<Cut>>')
    
    def copy(self):
        self.text.event_generate('<<Copy>>')
    
    def paste(self):
        self.text.event_generate('<<Paste>>')
    
    def select_all(self):
        self.text.tag_add('sel', '1.0', 'end')
        return 'break'
    
    def _on_key_release(self, event=None):
        self.highlight_syntax()
        self.line_numbers.redraw()
    
    def _on_focus_in(self, event):
        self.highlight_syntax()
    
    def _on_focus_out(self, event):
        pass
    
    def highlight_syntax(self, event=None):
        if not hasattr(self, 'lexer'):
            return
            
        # Get the text
        text = self.text.get('1.0', 'end-1c')
        if not text.strip():
            return
        
        # Clear previous tags
        for tag in self.text.tag_names():
            if tag != 'sel' and tag != 'current_line':
                self.text.tag_remove(tag, '1.0', 'end')
        
        # Lex the text
        try:
            tokens = list(lex(text, self.lexer))
            
            # Apply highlighting
            for token in tokens:
                token_type = token[0]
                token_text = token[1]
                start = token[2][0] - 1  # Convert to 0-based index
                line = token[2][1]
                
                if not token_text.strip():
                    continue
                    
                # Calculate start and end positions
                start_pos = f"{line}.{token[2][2]}"
                end_pos = f"{line}.{token[2][2] + len(token_text)}"
                
                # Apply the tag
                tag_name = str(token_type)
                if tag_name not in self.text.tag_names():
                    self.text.tag_configure(tag_name, foreground='#D4D4D4')
                
                self.text.tag_add(tag_name, start_pos, end_pos)
                
        except Exception as e:
            # If there's an error in lexing, just continue without highlighting
            pass
    
    def get(self, *args, **kwargs):
        return self.text.get(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        return self.text.delete(*args, **kwargs)
    
    def insert(self, *args, **kwargs):
        return self.text.insert(*args, **kwargs)
    
    def edit_undo(self):
        try:
            self.text.edit_undo()
        except tk.TclError:
            pass
    
    def edit_redo(self):
        try:
            self.text.edit_redo()
        except tk.TclError:
            pass
    
    def event_generate(self, *args, **kwargs):
        return self.text.event_generate(*args, **kwargs)
    
    def tag_add(self, *args, **kwargs):
        return self.text.tag_add(*args, **kwargs)
    
    def tag_remove(self, *args, **kwargs):
        return self.text.tag_remove(*args, **kwargs)
    
    def tag_configure(self, *args, **kwargs):
        return self.text.tag_configure(*args, **kwargs)
    
    def tag_names(self, *args, **kwargs):
        return self.text.tag_names(*args, **kwargs)
