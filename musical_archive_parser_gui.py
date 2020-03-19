from tkinter import *
from tkinter.scrolledtext import ScrolledText

root = Tk()
root.title("Musical archives parser")

entry_row = Frame(root)

select_btn = Button(entry_row, text="...")
select_btn.pack(side=RIGHT)

ent = Entry(entry_row)
ent.pack(side=LEFT, expand=YES, fill=X)

entry_row.pack(side=TOP, fill=X)

st = ScrolledText(root)
st.pack(side=TOP, expand=YES, fill=BOTH)

extract_btn = Button(root, text="Extract")
extract_btn.pack(side=LEFT)

root.mainloop()
