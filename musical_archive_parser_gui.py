from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory

root = Tk()
root.title("Musical archives parser")

def on_select_btn_click():
    directory = askdirectory()
    if directory != None:
        ent.insert(0, directory)


entry_row = Frame(root)

select_btn = Button(entry_row, text="...", command=on_select_btn_click)
select_btn.pack(side=RIGHT)

ent_name = Label(entry_row, text="Directory:")
ent_name.pack(side=LEFT)

ent = Entry(entry_row)
ent.pack(side=TOP, expand=YES, fill=X)

entry_row.pack(side=TOP, fill=X)


st = ScrolledText(root)
st.pack(side=TOP, expand=YES, fill=BOTH)


extract_btn = Button(root, text="Extract")
extract_btn.pack(side=LEFT)

root.mainloop()
