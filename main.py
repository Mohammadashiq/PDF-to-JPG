from tkinter.ttk import Progressbar

from pdf2image import convert_from_path
from tkinter import *
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox, filedialog, ttk
import threading
import time




class Converter:
    def __init__(self):
        self.window = Tk()
        self.window.title("PDF to JPG Converter")
        self.window.geometry("280x330")
        self.window.resizable(False, False)
        self.selected_pdf = []
        self.pdf_list = []
        self.output_folder = open("output.txt", "r").readline()
        self.menu_bar = self.create_top_menu()
        self.frame1, self.frame2 = self.create_frames()
        self.create_frame1_labels()
        self.create_frame1_buttons()
        self.list = self.create_records_list()
        self.create_frame2_buttons()

    def create_frames(self):
        frame1 = Frame(self.window)
        frame1.grid(row=0, column=0, pady=10)
        frame2 = Frame(self.window)
        frame2.grid(row=1, column=0, padx=20)
        return frame1, frame2

    def create_frame1_labels(self):
        label = Label(self.frame1, text="PDF to JPG", font=('Tahoma', 10))
        label.grid(row=0, column=0)

    def create_frame1_buttons(self):
        add_button = Button(self.frame1, text="Select PDF", command=self.select_pdf)
        add_button.grid(row=0, column=1, padx=5)
        clear_button = Button(self.frame1, text="Clear", command=self.clear_pdf)
        clear_button.grid(row=0, column=2)

    def create_frame2_buttons(self):
        convert_button = Button(self.frame2, text="Convert", command=self.start_thread)
        convert_button.grid(row=1, column=0, pady=5)

    def start_thread(self):
        thread = threading.Thread(target=self.convert_pdf)
        thread.start()

    def create_top_menu(self):
        menu_bar = Menu(self.window)
        app_menu = Menu(menu_bar, tearoff=0)
        app_menu.add_command(label="Save Location", command=self.select_folder)
        menu_bar.add_cascade(label="Settings", menu=app_menu)
        return self.window.config(menu=menu_bar)

    def select_folder(self):
        folder = filedialog.askdirectory()
        self.output_folder = open("output.txt", "w").write(folder)
        self.output_folder = open("output.txt", "r").readline()

    def select_pdf(self):
        self.selected_pdf = askopenfilenames(title='Choose a file')
        for pdf in self.selected_pdf:
            pdf_name = pdf.split("/")[-1]
            name = pdf_name.split(".")[-2]
            self.list.insert(parent='', index='end', text='', values=(name, ), )
            self.pdf_list.append(pdf)

    def convert_pdf(self):

        for n, pdf in enumerate(self.pdf_list):
            pdf_name = pdf.split("/")[-1]
            name = pdf_name.split(".")[-2]
            images = convert_from_path(pdf, dpi=300, poppler_path=r"G:\poppler-0.68.0\bin")
            for i in range(len(images)):
                images[i].save(f'{self.output_folder}/{name} page{i}.jpg', 'JPEG')
        messagebox.showinfo("Success", "Convert completed!!!")

    def create_records_list(self):
        list_y_scroll = Scrollbar(self.frame2)
        list_y_scroll.grid(row=0, column=1, sticky='ns')
        records_tree = ttk.Treeview(self.frame2, yscrollcommand=list_y_scroll.set, selectmode="extended")
        records_tree.grid(row=0, column=0)
        list_y_scroll.config(command=records_tree.yview)
        records_tree['columns'] = "PDF"
        records_tree.column("#0", width=0, stretch=NO)
        records_tree.heading("#0", text="", anchor=W)

        records_tree.column("PDF", width=230)
        records_tree.heading("PDF", text="Selected PDF's")
        return records_tree

    def clear_pdf(self):
        for n in self.pdf_list:
            self.pdf_list.remove(n)
        for n in self.list.get_children():
            self.list.delete(n)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    c = Converter()
    c.run()

