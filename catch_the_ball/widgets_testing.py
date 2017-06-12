from tkinter import *

def button1_command():
    print ('Button 1 default ocmmand')


def print_hello(event):
    me = event.widget
    print(event.num)
    print(event.x, event.y)
    if me == button1:
        print('Hello!')
    elif me == button2:
        print('You pressed button2')
    else:
        raise ValueError()


def init_main_window():
    #Инициализация главного окна. Создание виджетов и упаковка
    global root, button1, button2, label, text, scale
    root = Tk()

    button1 = Button(root, text = 'Button 1', command=button1_command)
    button1.bind('<Button>', print_hello)

    button2 = Button(root, text = 'Button 2')
    button2.bind('<Button>', print_hello)

    variable = IntVar(0)
    label = Label(root, textvariable=variable)
    scale = Scale(root, orient=HORIZONTAL, length=300, from_=0, to=100, tickinterval=10, resolution=5, variable=variable)
    text = Entry(root, textvariable=variable)

    for obj in button1, button2, label, scale, text:
        obj.pack()

if __name__ == '__main__':
    init_main_window()

    root.mainloop()
