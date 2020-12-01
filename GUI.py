"""
Graphical user interface for the photo sorter allowing:
- Choose source and destination directories
- Set the source directory's address for the output
- See log of the program's work in the text box
"""

from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from sorter import sort_photos


def choose_source_dir():
    """
    Asks user to choose the source directory and puts the path to the entry box
    :return:
    """
    source_dir_name = fd.askdirectory()
    source_entry.delete(0, END)
    source_entry.insert(0, source_dir_name)


def choose_result_dir():
    """
    Asks user to choose the destination directory and puts the path to the entry box
    :return:
    """
    result_dir_name = fd.askdirectory()
    result_entry.delete(0, END)
    result_entry.insert(0, result_dir_name)


def set_same_path():
    """
    Makes the destination path the same as the source path
    :return:
    """
    path = source_entry.get()
    result_entry.delete(0, END)
    result_entry.insert(0, path)


def execute():
    """
    Calls the sort function with 2 args: source and destination directories
    Before calling the function checks if source and destination directories are entered
    :return:
    """
    input_dir = source_entry.get()
    if not input_dir:
        mb.showerror("Error", "Choose source directory")

    output_dir = result_entry.get()
    if not output_dir:
        mb.showerror("Error", "Choose output directory")

    if input_dir and output_dir:
        sort_photos(input_dir, output_dir)


def redirector(input_str):
    """
    Gets a string and inserts it into the text box
    :param input_str:
    :return:
    """
    log_text.insert(END, input_str)


sys.stdout.write = redirector  # whenever sys.stdout.write is called, redirector is called

root = Tk()
root.title("Photo Sorter")
root.resizable(False, False)
root.geometry('600x600')

f_1 = Frame(root)
f_2 = Frame(root)
f_3 = Frame(root)

source_entry = Entry(f_1, width=60)
result_entry = Entry(f_2, width=60)


log_text = Text(width=200, height=100)

source_button = Button(f_1, width=15, text='Source directory', command=choose_source_dir)
result_button = Button(f_2, width=15, text='Output directory', command=choose_result_dir)
start_button = Button(f_3, width=20, text='Sort photos', command=execute)

same_path_bool = BooleanVar()
same_path_bool.set(0)
same_path_button = Checkbutton(f_3, text="Output to source directory", variable=same_path_bool,
                               onvalue=1, command=set_same_path)


f_1.pack()
f_2.pack()
f_3.pack()

source_button.pack(side=LEFT)
result_button.pack(side=LEFT)

source_entry.pack(ipady=3)
result_entry.pack(ipady=3)

same_path_button.pack(side=LEFT)
start_button.pack()

log_text.pack()


root.mainloop()
