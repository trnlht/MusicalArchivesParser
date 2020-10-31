from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import askdirectory
from subprocess import Popen, PIPE
import _thread 
import os, queue
import pdb

#TODO Добавить вывод наденных архивов перед парсингом
#TODO Добавить вывод списка архивов которые не удалось распарсить

#TODO Добавить горизонтальный скролл в ScrolledText из tkinter (?)
#TODO Проверять путь к папке перед извлечением (?)

class MusicalArchivesParserGui(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.pack(expand=YES, fill=BOTH)
        self.create_widgets()
        self.master.title("Musical archives parser")
        self.msg_queue = queue.Queue()

    def create_widgets(self):
        entry_row = Frame(self)

        select_btn = Button(entry_row, text="...", command=self.on_select_btn_click)
        select_btn.pack(side=RIGHT)

        ent_name = Label(entry_row, text="Directory:")
        ent_name.pack(side=LEFT)

        self.ent = Entry(entry_row)
        self.ent.pack(side=TOP, expand=YES, fill=X)

        entry_row.pack(side=TOP, fill=X)

        text_frame = Frame(self)
        self.text = Text(text_frame, wrap="none")
        vbar = Scrollbar(text_frame)
        hbar = Scrollbar(text_frame, orient="horizontal")

        vbar.pack(side=RIGHT, fill=Y)
        hbar.pack(side=BOTTOM, fill=X)
        self.text.pack(side=TOP, fill=BOTH, expand=YES)

        self.text.config(yscrollcommand=vbar.set)
        self.text.config(xscrollcommand=hbar.set)
        vbar.config(command=self.text.yview)
        hbar.config(command=self.text.xview)

        text_frame.pack(side=TOP, expand=YES, fill=BOTH)
        
        # self.st = ScrolledText(self, wrap=NONE)
        # self.st.pack(side=TOP, expand=YES, fill=BOTH)

        extract_btn = Button(self, text="Extract", command=self.on_extract_btn_click)
        extract_btn.pack(side=LEFT)

    def parser_output_reader(self, parser_output):
        while True:
            line = parser_output.readline()
            self.msg_queue.put(line)
            if not line:
                break

    def parser_output_writer(self):
        try:
            line = self.msg_queue.get(block=False)
        except queue.Empty:
            pass
        else:
            if not line:
                return
            self.text.insert(END, line)
        self.after(250, lambda: self.parser_output_writer())

    def on_select_btn_click(self):
        directory = askdirectory()
        if directory != None:
            self.ent.insert(0, directory)

    def on_extract_btn_click(self):
        # Чтение пути к папке из поля ввода и передача его запускаемому скрипту 
        archives_path = self.ent.get()
        p = Popen(["python", "-u", "musicalArchivesParser.py", archives_path], stdout=PIPE)
        _thread.start_new_thread(self.parser_output_reader, (p.stdout,))
        self.parser_output_writer()


if __name__ == "__main__":
    MusicalArchivesParserGui().mainloop()
