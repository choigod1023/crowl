from tkinter import *
import threading
from queue import Queue
window = Tk()
lock = threading.Lock()
class vlive():
    def vlive_download(q,self):
        evt = threading.Event()
        print('wait...')
        lock.acquire()
        print(str.get())
        lock.release()
        print('done')
        
    def vlive_toplevel(self):
        f1 = Toplevel(window)
        l1 = Label(f1, text="주소") # Label:텍스트 표시
        l1.grid(row=0, column=0)
        global str
        str = StringVar()
        e1 = Entry(f1,textvariable = str) # Entry:사용자로부터 입력 받는 부분
        e1.grid(row=0, column=1)
        
        b1 = Button(f1,text="다운로드!",command=thread1.start)
        b1.grid(row=0,column=2)

q=Queue(10)
menubar=Menu(window)
vl = vlive()
filemenu=Menu(menubar,tearoff=0)
thread1 = threading.Thread(target=vl.vlive_download,args=(q,))
filemenu.add_command(label="VLIVE",command=vl.vlive_toplevel)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=window.quit)


menubar.add_cascade(label="메뉴",menu=filemenu)


window.config(menu=menubar)

window.mainloop()