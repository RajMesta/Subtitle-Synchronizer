from tkinter import *
import tkinter.ttk as ttk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import re

root = Tk()
root.title("Sub Synco")
width = 1000
height = 600
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.config(bg="#C19A92")

Top = Frame(root, width=500, bd=3, relief=SOLID)
Top.pack(side=TOP)
files = Frame(root, width=500, padx=10, pady=10)
files.pack(fill=X)
TableMargin = Frame(root, width=500)
TableMargin.pack(side=TOP)
start_time_input = Entry(files, width=30)
start_time_input.pack()

def change_time(t):
    return int(t[ 9:12 ]) + 1000 * (int(t[ 6:8 ]) + 60 * (int(t[ 3:5 ]) + 60 * int(t[ 0:2 ])))

def add_time(t,to_add):
    time = t + to_add
    hr = time//3600000
    time = time%3600000
    m = time//60000
    time = time%60000
    sec = time//1000
    msec = time%1000
    return str(hr).zfill(2)+':'+str(m).zfill(2)+':'+str(sec).zfill(2)+','+str(msec).zfill(3)

def fill_tree():
    global pth
    f = open(pth, "r")
    tree.delete(*tree.get_children())
    data = []
    txt = ''
    for i in f:
        pat1 = '[0-9]+'
        pat2 = '^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
        if re.match(pat2, i):
            start = i[ :12 ]
            end = i[ -13:-1]
            data.append(start)
            data.append(end)
        elif re.match(pat1, i[:-1]):
            data.append(i[:-1])
        else:
            txt += i
        if (len(data) == 4):
            val = [ data[ 0 ], data[ 1 ], txt.replace('\n',' '), data[ 2 ] ]
            data = [ data[ 3 ] ]
            txt = ''
            tree.insert('', 'end', values=tuple(val))

def select():
    global pth
    pth = filedialog.askopenfilename()
    path = pth.split('/')
    path = path[ -1 ].split('.')
    if (path[ 1 ] != "srt"):
        tkMessageBox.showwarning('', 'Please Select SRT file', icon="warning")
    else:
        title.config(text=path[ 0 ])
        title.pack(side=BOTTOM)
        update.pack(side=BOTTOM)
        fill_tree()

def update():
    t1 = start_time_input.get()
    global pth
    f = open(pth, "r")
    for i in f:
        pat = '[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
        if re.match(pat, i):
            t2 = i[ :12 ]
            global to_add
            to_add = change_time(t1) - change_time(t2)
            break
    tree.delete(*tree.get_children())
    f = open(pth, "r")
    data = []
    txt = ''
    for i in f:
        pat1 = '[0-9]+'
        pat2 = '^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
        if re.match(pat2, i):
            start = i[ :12 ]
            end = i[ -13:-1 ]
            start = change_time(start)
            end = change_time(end)
            data.append(add_time(start,to_add))
            data.append(add_time(end,to_add))
        elif re.match(pat1, i[:-1]):
            data.append(i[ :-1 ])
        else:
            txt += i
        if (len(data) == 4):
            val = [ data[0], data[1], txt.replace('\n', ' '), data[2] ]
            data = [ data[ 3 ] ]
            txt = ''
            tree.insert('', 'end', values=tuple(val))

def save():
    f = open("Spirited Away.srt", "r")
    new = open(pth,"w+")
    global to_add
    for i in f:
        pat = '^[0-9]{2}:[0-9]{2}:[0-9]{2},[0-9]{3}'
        if re.match(pat, i):
            start = i[ :12 ]
            end = i[ -13: ]
            start = change_time(start)
            end = change_time(end)
            new.write(add_time(start, to_add) + ' --> ' + add_time(end, to_add))
            new.write('\n')
        else:
            new.write(i)
    tkMessageBox.showinfo('','File saved succesfully!!')

title = Label(files, text="", font=("arial", 20), fg="#EC2519")
save_file = Button(files, text="SAVE FILE", bg="#66ff66", command=save).pack(side=RIGHT)
choose_file = Button(files, text="CHOOSE FILE", bg="#75C3F1", command=select).pack(side=LEFT)
l = Label(files, text="Enter the start time    Format:- 02:00:53,546", font=("arial", 11)).pack()
update = Button(files, text="UPDATE", bg="orange", command=update)



lbl_title = Label(Top, text="Subtitle Synchronizer", font=('arial', 16), width=500, fg="#F4F0F5", bg="#8F25C0")
lbl_title.pack(fill=X)

style = ttk.Style()
style.configure("mystyle.Treeview", highlightthickness=0, font=('Calibri', 11))  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", bd=0, font=('Calibri', 13, 'bold'))  # Modify the font of the headings
style.layout("mystyle.Treeview", [ ('mystyle.Treeview.treearea', {'sticky': 'nswe'}) ])  # Remove the borders

scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
tree = ttk.Treeview(TableMargin, columns=("#1", "#2", "#3", "#4"),
                    height=400, selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set,
                    style="mystyle.Treeview")
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('#1', text="Index")
tree.heading('#2', text="Start Time")
tree.heading('#3', text="Text")
tree.heading('#4', text="End Time")
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=60)
tree.column('#2', stretch=NO, minwidth=0, width=150)
tree.column('#3', stretch=NO, minwidth=0, width=469)
tree.column('#4', stretch=NO, minwidth=0, width=150)
tree.pack()

root.mainloop()
