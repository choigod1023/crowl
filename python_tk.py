from tkinter import *
import threading
from queue import Queue
window = Tk()
def vlive_download():
    print('wait...')
    print(str.get())
    print('done')
        
def vlive_toplevel():
    f1 = Toplevel(window)
    l1 = Label(f1, text="주소") # Label:텍스트 표시
    l1.grid(row=0, column=0)
    global str
    str = StringVar()
    e1 = Entry(f1,textvariable = str) # Entry:사용자로부터 입력 받는 부분
    e1.grid(row=0, column=1)
        
    b1 = Button(f1,text="다운로드!",command=vlive_download)
    b1.grid(row=0,column=2)

menubar=Menu(window)
filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="VLIVE",command=vlive_toplevel)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=window.quit)


menubar.add_cascade(label="메뉴",menu=filemenu)


window.config(menu=menubar)

window.mainloop()