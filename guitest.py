from tkinter import *
from tkinter import ttk
import pyperclip
import ctypes

# Global variables for styles
BG_COLOR = 'black'
BTN_COLOR = '#006400'
BTN_ACTIVE_COLOR = '#004d00'
ENTRY_BG_COLOR = '#006400'
FONT = ("Courier", 10, "bold")
TEXT_COLOR = 'black'
PLACEHOLDER_COLOR = 'black'

# Load the strclib.dll library
strclib = ctypes.CDLL(r"C:\Users\nicol\OneDrive\Escritorio\PassGen\strclib.dll")

# Define the Caesar cipher function in ctypes
# void encryption_cesar(char *input, int key);
encryption_cesar = strclib.encryption_cesar
encryption_cesar.argtypes = [ctypes.c_char_p, ctypes.c_int]

def generate_password(keyword, keynumber):
    # Example logic for password generation using the Caesar cipher function
    input_text = keyword.encode('utf-8')
    key = int(keynumber)
    output_text = ctypes.create_string_buffer(len(input_text) + 1)  # +1 for null terminator
    ctypes.memmove(output_text, input_text, len(input_text))
    encryption_cesar(output_text, key)
    password = output_text.value.decode('utf-8')
    return password

def update_password():
    pwd = generate_password(key_word.get(), key_number.get())
    password.set(pwd)

def copy_to_clipboard():
    pyperclip.copy(password.get())

def add_placeholder(entry, placeholder_text):
    entry.insert(0, placeholder_text)
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder_text))
    entry.bind("<FocusOut>", lambda event: set_placeholder(entry, placeholder_text))
    entry.config(foreground=PLACEHOLDER_COLOR)

def clear_placeholder(entry, placeholder_text):
    if entry.get() == placeholder_text:
        entry.delete(0, END)
        entry.config(foreground=TEXT_COLOR)

def set_placeholder(entry, placeholder_text):
    if entry.get() == "":
        entry.insert(0, placeholder_text)
        entry.config(foreground=PLACEHOLDER_COLOR)

def center_window(root, width, height):
    # Get screen dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate x, y coordinates to center the window
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    
    # Set window geometry
    root.geometry(f"{width}x{height}+{x}+{y}")

root = Tk()
root.title("PASSGEN")
root.configure(bg=BG_COLOR)

# Adjust window size and position to be centered
window_width = 650
window_height = 300
center_window(root, window_width, window_height)

# Prevent window from being resizable
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

# Style for borderless buttons
style.configure("TButton", background=BTN_COLOR, foreground=TEXT_COLOR, font=FONT, borderwidth=0, relief="flat")
style.map("TButton",
    background=[('active', BTN_ACTIVE_COLOR)],
    foreground=[('active', TEXT_COLOR)])

# Style for entry fields
style.configure("TEntry", fieldbackground=ENTRY_BG_COLOR, background=BG_COLOR, foreground=TEXT_COLOR, font=FONT, relief="flat")
style.map("TEntry",
    fieldbackground=[('active', ENTRY_BG_COLOR)],
    foreground=[('active', TEXT_COLOR)])

# Adjust the height of Entry widgets to match buttons
style.configure("Custom.TEntry", padding=[5, 5], borderwidth=0)

# Style for the footer
style.configure("Footer.TFrame", background=BG_COLOR)
style.configure("Footer.TLabel", background=BG_COLOR, foreground=BTN_COLOR, font=FONT)

mainframe = ttk.Frame(root, padding="20 20 20 20", style="Mainframe.TFrame")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

style.configure("Mainframe.TFrame", background=BG_COLOR) # Black background for mainframe
style.configure("TLabel", background=BG_COLOR, foreground="white") # White text on black background

# Configure internal padding for widgets
padding_args = {'padx': 10, 'pady': 10}

key_word = StringVar()
key_word_entry = ttk.Entry(mainframe, width=40, textvariable=key_word, style="Custom.TEntry")
key_word_entry.grid(column=1, row=1, sticky=(W, E), **padding_args)
add_placeholder(key_word_entry, "Key word")

key_number = StringVar()
key_number_entry = ttk.Entry(mainframe, width=20, textvariable=key_number, style="Custom.TEntry")
key_number_entry.grid(column=2, row=1, sticky=(W, E), **padding_args)
add_placeholder(key_number_entry, "Key number")

password = StringVar()
password_label = ttk.Label(mainframe, textvariable=password)
password_label.grid(column=1, row=2, columnspan=2, sticky=(W, E), **padding_args)

generate_button = ttk.Button(mainframe, text='Generate password', command=update_password)
generate_button.grid(column=3, row=1, **padding_args)

copy_button = ttk.Button(mainframe, text='Copy to clipboard', command=copy_to_clipboard)
copy_button.grid(column=3, row=2, **padding_args)

# Create the footer
footer = ttk.Frame(root, style="Footer.TFrame")
footer.grid(column=0, row=1, sticky=(W, E))
footer.columnconfigure(0, weight=1)

footer_label = ttk.Label(footer, text="Nicolas Martin Catania © 2024", style="Footer.TLabel")
footer_label.grid(column=0, row=0, pady=10)

# Expand columns and rows to take available space
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

mainframe.grid_columnconfigure(0, weight=1)
mainframe.grid_columnconfigure(1, weight=1)
mainframe.grid_columnconfigure(2, weight=1)
mainframe.grid_columnconfigure(3, weight=1)

mainframe.grid_rowconfigure(0, weight=1)
mainframe.grid_rowconfigure(1, weight=1)
mainframe.grid_rowconfigure(2, weight=1)
mainframe.grid_rowconfigure(3, weight=1)
mainframe.grid_rowconfigure(4, weight=1)

root.mainloop()
