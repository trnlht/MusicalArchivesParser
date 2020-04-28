from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory
from subprocess import Popen, PIPE
import _thread 
import os, queue
import pdb

def parser_output_reader(parser_output):
    while True:
        line = parser_output.readline()
        msg_queue.put(line)
        if not line:
            break

def parser_output_writer(root):
    try:
        line = msg_queue.get(block=False)
    except queue.Empty:
        pass
    else:
        if not line:
            st.insert(END, "<end>")
            return
        st.insert(END, line)
    root.after(250, lambda: parser_output_writer(root))


def on_select_btn_click():
    directory = askdirectory()
    if directory != None:
        ent.insert(0, directory)

def on_extract_btn_click():
    
    # Чтение пути к папке из поля ввода и передача его запускаемому скрипту 
    archives_path = ent.get()
    p = Popen(["python", "-u", "musicalArchivesParser.py", archives_path], stdout=PIPE)
    _thread.start_new_thread(parser_output_reader, (p.stdout,))
    parser_output_writer(root)

msg_queue = queue.Queue()

root = Tk()
root.title("Musical archives parser")

entry_row = Frame(root)

select_btn = Button(entry_row, text="...", command=on_select_btn_click)
select_btn.pack(side=RIGHT)

ent_name = Label(entry_row, text="Directory:")
ent_name.pack(side=LEFT)

ent = Entry(entry_row)
ent.pack(side=TOP, expand=YES, fill=X)

entry_row.pack(side=TOP, fill=X)


st = ScrolledText(root, wrap=NONE)
st.pack(side=TOP, expand=YES, fill=BOTH)


extract_btn = Button(root, text="Extract", command=on_extract_btn_click)
extract_btn.pack(side=LEFT)

root.mainloop()
