from turtle import width
from numpy import add
import unwebpCore as ucore
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import font as tkfont

#using tk create a gui
#it lets user create a file list by adding one or more files via browse button
#it lets user select a directory to save the files to
#it lets user select a format to save the files to
#it then goes through the list of files, converts them and saves them to the selected directory
#then displays a message if everything went well or not
#a function that opens a file browser and adds the selected files to the list
#once the user selects the files, if they aren't already in the list they will be added
def add_files():
    i = 0
    added_files = 0
    #open a file browser
    #start_dir = ucore.os.curdir
    ucore.debug("Adding files...")
    start_dir = "/"
    files = fd.askopenfilenames(initialdir=start_dir, title="Select files to convert", filetypes=(("all files","*.*"),("webp", "*.webp"), ("png", "*.png"), ("jpg", "*.jpg"), ("jpeg", "*.jpeg")))
    #add the files to the list
    ucore.debug("Selected files: "+str(len(files)))
    for file in files:
        i += 1
        #check if the file is already in the list
        if file not in selected_files_list.get(0,tk.END):
            selected_files_list.add_item(file)
            ucore.debug(str(i)+". Added file: "+str(file))
            added_files+=1
        else:
            ucore.debug(str(i)+". File already in list: "+str(file))
    #update the selected files variable
    
    ucore.debug("Added files: "+str(added_files))
    complete_label.configure(text="")
    
    
#a function that allows to specify a directory to save the files to
def select_directory():
    start_dir = ucore.os.curdir+ucore.uvars.output_directory
    real_directory = ucore.uvars.get_real_dir()
    if real_directory == "":
        save_dir_preview.configure(text=start_dir)
    #open a file browser
    directory = fd.askdirectory(initialdir=start_dir, title="Select a folder to save files")
    #update the selected directory variable
    save_dir_preview.configure(text=directory)
    ucore.uvars.set_real_dir(directory)
    ucore.debug("Save directory set to: "+ucore.uvars.get_real_dir())
    ucore.debug("Save directory label set to: "+save_dir_preview.cget("text"))
    complete_label.configure(text="")




def reset_directory():
    save_dir_preview.configure(text="(Saving to source)")
    #get parent script name
    ucore.uvars.set_real_dir("")
    ucore.debug("Save directory reset: "+ucore.uvars.get_real_dir())
    ucore.debug("Save directory label set to: "+save_dir_preview.cget("text"))
    complete_label.configure(text="")
    


#function iterates through a list of files and converts them
def convert_list():
    #get the list of files
    files = selected_files_list.get(0,tk.END)
    #get the selected directory
    directory_info = save_dir_preview.cget("text")
    real_directory = ucore.uvars.get_real_dir()
    #get the selected format
    format = format_menu.get()
    ucore.debug("files to convert: "+str(files))
    ucore.debug("directory to save to: "+directory_info)
    ucore.debug("format to save as: "+format)
    #iterate through the list of files
    complete_label.configure(text="Converting...")
    ucore.debug("Converting...")
    i = 0
    for file in files:
        i += 1
        ucore.open_process_save_image(file, format, real_directory)
        progress = str(i)+"/"+str(len(files))+" files converted"
        complete_label.configure(text=progress)
    clear_list()
    complete_label.configure(text="Conversion complete!")
        
def clear_list():
    selected_files_list.delete(0,tk.END)
    ucore.debug("List cleared")
    complete_label.configure(text="")
        

#adds a scrollable list class
class MovListbox(tk.Listbox):
    s = None
    def __init__(self, master=None, inputlist=None, width=None, height=None, row=0,column=0):
        super(MovListbox, self).__init__(master=master)
        self.configure(width=width, height=height)
        # Populate the listbox with the inputlist
        for item in inputlist:
            self.insert(tk.END, item)

        #set scrollbar
        s = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.yview)
        self.configure(yscrollcommand=s.set)    
        self.grid(row=row, column=column)
        s.grid(row=row, column=column+1, sticky=tk.NS)  

    
    def add_item(self, item):
        self.insert(tk.END, item)
        


#create a window
window = tk.Tk()
window.title("Unwebp WEBP - JPG - PNG Converter")
window.geometry("500x500")
#sets up fonts
default_font = tkfont.nametofont("TkDefaultFont")
list_font = tkfont.nametofont("TkFixedFont")
default_font.configure(size=9)
#window.option_add("*Font", default_font)
mainframe = ttk.Frame(window, padding="20 20 20 20")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
###SELECT FILES
path_label = tk.Label(mainframe, text="Select files to convert")
path_label.grid(column=2, row=1, sticky=tk.W)

#add a browse button to select files
browse_files_button = ttk.Button(mainframe, text="Add Files", command=add_files)
browse_files_button.grid(column=2, row=2, sticky=(tk.W,tk.E))

###SELECT FORMAT
format_label = tk.Label(mainframe, text="Select output format")
format_label.grid(column=2, row=4, sticky=tk.W)

format = tk.StringVar()
format_menu = ttk.Combobox(mainframe, textvariable=format, state='readonly')
format_menu['values'] = ('jpg','png', 'webp', 'jpeg')
format_menu.current(0)
format_menu.grid(column=2, row=5, sticky=(tk.W, tk.E))

save_dir_preview = tk.Label(mainframe, text="(Saving to source)")
save_dir_preview.grid(column=2, row=6, sticky=tk.W)

#add a browse button to select save directory
browse_save_dir_button = ttk.Button(mainframe, text="Select save directory", command=select_directory)
browse_save_dir_button.grid(column=2, row=7, sticky=(tk.W,tk.E))
#add a reset save button
reset_save_dir_button = ttk.Button(mainframe, text="Save to source directory (reset folder)", command=reset_directory)
reset_save_dir_button.grid(column=2, row=8, sticky=(tk.W,tk.E))




###CHOSEN FILES
selected_files_label = tk.Label(mainframe, text="Selected files:")
selected_files_label.grid(column=2, row=9, sticky=tk.W)

#create a list to store the selected files
selected_files = []
selected_files_list = MovListbox(mainframe, inputlist=selected_files, width=75, height=10, column=2, row=10)
selected_files_list.grid(sticky=(tk.N, tk.W, tk.E))


#add a convert button that will start the process
convert_button = ttk.Button(mainframe, text="Convert", command=convert_list)
convert_button.grid(column=2, row=11, sticky=(tk.W,tk.E))

#add clear table list button
clear_list_button = ttk.Button(mainframe, text="Clear file list", command=clear_list)
clear_list_button.grid(column=2, row=13, sticky=(tk.W,tk.E))

#add a large text complete
complete_label = tk.Label(mainframe, text="")
complete_label.grid(column=2, row=14, sticky=(tk.W, tk.E))




window.mainloop()


    

    
