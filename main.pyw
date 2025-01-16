import customtkinter as tk
from customtkinter import filedialog
from CTkMessagebox import CTkMessagebox
from CTkListbox import CTkListbox
import shutil
import os
import configparser

script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'config.ini')

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        listbox_files.insert(tk.END, file_path)

def remove_selected_items():
    # Files listbox
    selected_files = listbox_files.curselection()
    if selected_files != None :
        listbox_files.delete(selected_files)

    # Output paths listbox
    selected_output_paths = listbox_output_paths.curselection()
    if selected_output_paths != None :
        listbox_output_paths.delete(selected_output_paths)

    # Executables listbox
    selected_executables = listbox_executables.curselection()
    if selected_executables != None :
        listbox_executables.delete(selected_executables)



def browse_output_path():
    output_path = filedialog.askdirectory()
    if output_path:
        listbox_output_paths.insert(tk.END, output_path)

def apply_settings():
    output_paths = listbox_output_paths.get("all")  
    files = listbox_files.get("all") 
    open_exes = var_open_exes.get()

    print(f"Files selected: {files}")
    print(f"Output paths selected: {output_paths}")

    if not files or not output_paths:
        CTkMessagebox(title="Error", message="File and Output must be filled")
        return
    
    try:
        for output_path in output_paths:
            for file_path in files:
                file_name = os.path.basename(file_path)
                shutil.copy(file_path, os.path.join(output_path, file_name))
        
        if open_exes:
            executables = listbox_executables.get("all")  
            for exe in executables:
                os.startfile(exe)
    except Exception as e:
        CTkMessagebox(title="Error", message=f"Failed to copy files or open executables: {str(e)}")



def save_settings():
    config = configparser.ConfigParser()

    # Files
    files = listbox_files.get("all")
    if files is None:
        files = []  
    config['Files'] = {f'file_{i}': exe for i, exe in enumerate(files)}

    # OutputPaths 
    output_paths = listbox_output_paths.get("all")
    if output_paths is not None:
        output_paths = ["".join(output_paths[i:i+1]) for i in range(len(output_paths))]  
    config['OutputPaths'] = {f'output_{i}': path for i, path in enumerate(output_paths)}

    # Executables
    executables = listbox_executables.get("all")
    if executables is None:
        executables = []  # Eğer None dönerse, boş liste kullan
    config['Executables'] = {f'exe_{i}': exe for i, exe in enumerate(executables)}

    # Settings
    config['Settings'] = {'open_exes': var_open_exes.get()}

    # Dosyaya yaz
    with open(config_file, 'w') as configfile:
        config.write(configfile)

    root.destroy()



def load_settings():
    if os.path.exists(config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        
        # Files
        if 'Files' in config:
            for key in sorted(config['Files']):
                listbox_files.insert(tk.END, config['Files'][key])

        # OutputPaths (Yolları birleştiriyoruz)
        if 'OutputPaths' in config:
            output_paths = []
            for key in sorted(config['OutputPaths']):
                output_paths.append(config['OutputPaths'][key])  # Yolu birleştir
            for path in output_paths:
                listbox_output_paths.insert(tk.END, path)

        # Executables
        if 'Executables' in config:
            for key in sorted(config['Executables']):
                listbox_executables.insert(tk.END, config['Executables'][key])

        # Settings
        if 'Settings' in config:
            var_open_exes.set(config['Settings'].getboolean('open_exes'))

def browse_executables():
    exe_path = filedialog.askopenfilename(filetypes=[("Executable files", "*.exe")]) # Use the extension you want to open
    if exe_path:
        listbox_executables.insert(tk.END, exe_path)

# Main window
root = tk.CTk()
root.title("Build Manager")

# File List
lbl_files = tk.CTkLabel(root, text="Selected Files:")
lbl_files.grid(row=0, column=0, padx=10, pady=10)

listbox_files = CTkListbox(root, height=50)  # Hedeflenen argümanlar
listbox_files.grid(row=0, column=1, padx=10, pady=10)
btn_browse_file = tk.CTkButton(root, text="Browse", command=browse_file)
btn_browse_file.grid(row=0, column=2, padx=10, pady=10)

# Output Path List
lbl_output_paths = tk.CTkLabel(root, text="Selected Output Paths:")
lbl_output_paths.grid(row=2, column=0, padx=10, pady=10)

listbox_output_paths = CTkListbox(root, height=50)  # Hedeflenen argümanlar
listbox_output_paths.grid(row=2, column=1, padx=10, pady=10)
btn_browse_output_path = tk.CTkButton(root, text="Browse", command=browse_output_path)
btn_browse_output_path.grid(row=2, column=2, padx=10, pady=10)

# Executable List
lbl_executables = tk.CTkLabel(root, text="Executables:")
lbl_executables.grid(row=3, column=0, padx=10, pady=10)

listbox_executables = CTkListbox(root, height=50)  # Hedeflenen argümanlar
listbox_executables.grid(row=3, column=1, padx=10, pady=10)
btn_browse_executables = tk.CTkButton(root, text="Browse", command=browse_executables)
btn_browse_executables.grid(row=3, column=2, padx=10, pady=10)

btn_remove_selected = tk.CTkButton(root, text="Remove", command=remove_selected_items)
btn_remove_selected.grid(row=5, column=2, padx=10, pady=10)

# Checkbox for opening executables
var_open_exes = tk.BooleanVar()
chk_open_exes = tk.CTkCheckBox(root, text="Open Executables", variable=var_open_exes)
chk_open_exes.grid(row=4, column=1, padx=10, pady=10)

# Apply Button
btn_apply = tk.CTkButton(root, text="Apply", command=apply_settings)
btn_apply.grid(row=5, column=1, pady=20)

# Load settings
load_settings()
root.protocol("WM_DELETE_WINDOW", save_settings)
root.mainloop()
