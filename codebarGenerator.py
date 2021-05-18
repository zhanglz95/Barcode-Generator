from tkinter import *
from tkinter import filedialog
from codeUtils import getCanvas
import os
import tkinter as tk
import tkinter.messagebox
import codeUtils

def browse_button():
    dirpath = filedialog.askdirectory()
    pathStr.set(dirpath)
    return dirpath

def generate():
    codes = text.get('0.0','end').strip()
    if codes == "":
        tk.messagebox.showerror(title = '错误',message='请指定至少一行编码！')
        return
    path = pathStr.get().strip()
    if not os.path.isdir(path):
        tk.messagebox.showerror(title = '错误',message='请选择正确目录！')
        return
    filename = output_name_dir.get().strip()
    if filename == "":
        tk.messagebox.showerror(title = '错误',message='请指定文件名！')
        return
    if not filename.endswith(".pdf"):
        filename = filename + ".pdf"
    batch_number = batch_text.get().strip()
    codes = codes.split('\n')
    c = getCanvas(codes, path, filename, batch_number)
    try:
        c.save()
    except:
        tk.messagebox.showerror(title = '错误',message='发生未知错误！')
    else:
        tk.messagebox.showinfo('提示', '条形码已生成！')


def importFromFile():
    import_file = filedialog.askopenfilename(filetypes=[('TXT', '*.txt')])
    text.delete('1.0','end')
    with open(import_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            text.insert('end',line)


top = Tk()
top.title("条形码生成")
top.geometry("500x360")
path = os.path.dirname(os.path.abspath(__file__))

top.iconbitmap(os.path.join(path, "bitbug_favicon.ico"))

pathStr = StringVar()

label_input = Label(top, text="编码：")
text = Text(top, width=30, height=20, bd=2, undo=True)
import_btn = Button(top, activebackground="grey", height = 2, width=12, text = "从txt文本导入", command=importFromFile)

label_output_dir = Label(top, text="输出目录：")
output_dir = Entry(top, width = 25, textvariable=pathStr)
output_dir.configure(state='disabled')
output_browser_btn = Button(top, activebackground="grey", text = "浏览", width=5, command=browse_button)

label_file_name = Label(top, text="输出文件名(PDF)：")
output_name_dir = Entry(top, width = 25)

batch_str_name = Label(top, text="批次号：")
batch_text = Entry(top, width = 25)

generate_btn = Button(top, activebackground="grey", height = 2, width=12, text = "生成", command=generate)


label_input.place(x=10, y=5)
text.place(x=10, y=30)
import_btn.place(x=70, y=300)

label_output_dir.place(x=250, y=60)
output_dir.place(x=250, y=90)
output_browser_btn.place(x=440, y=85)

label_file_name.place(x=250, y=140)
output_name_dir.place(x=250, y=170)

batch_str_name.place(x = 250, y = 210)
batch_text.place(x = 250, y = 240)

generate_btn.place(x=300, y=300)

# 进入消息循环
top.mainloop()