from tkinter import *

def paint(event):
    '''Обработчик событий для холста
    '''
    print(event.x, event.y)
    if event.widget != canvas:
        print('Strange')
        return
    canvas.coords(line, 0, 0, event.x, event.y)

root = Tk()

canvas = Canvas(root, bg='white', width=400, height=400)
canvas.bind('<Motion>', paint)
canvas.pack()

line = canvas.create_line(0, 0, 10, 10)

for i in range(10):
    oval = canvas.create_oval(i*40, i*40, i*40+30, i*40+30, width=2, fill='green')

root.mainloop()
print('Exit from App')
