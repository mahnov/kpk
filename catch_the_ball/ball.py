from tkinter import *
from random import choice, randint

ball_initial_number = 10
ball_minimal_radius = 15
ball_maximal_radius = 40
ball_available_colors = ['green', 'blue', 'red', 'lightgreen', '#FF00FF', '#AAAA00']

def click_ball(event):
    '''Обработчик событий мышки для  игорового холста
    :param event: событие с координатами клика
    по клику мышкой нужно удалять объект, на который указывает мышка
    засчитывать шарик в очки пользователя
    '''
    obj = canvas.find_closest(event.x, event.y)
    x1, y1, x2, y2 =  canvas.coords(obj)
    if x1 <= event.x <= x2 and y1 <= event.y <= y2:
        canvas.delete(obj)
        #учесть объект в очках
        create_random_ball()
    #(event.x, event.y)

def move_all_balls(event):
    '''
    Передвигает все шарики
    '''
    for obj in canvas.find_all():
        dx = randint(-1, 1)
        dy = randint(-1, 1)
        canvas.move(obj, dx, dy)

def create_random_ball():
    '''
    Создает шарик в случайном месте холста canvas, при этом шарик не выходит за границы
    '''
    R = randint(ball_minimal_radius, ball_maximal_radius)
    x = randint(0, int(canvas['width'])-2*R-1)
    y = randint(0, int(canvas['height'])-2*R-1)
    canvas.create_oval(x, y, x+2*R, y+2*R, fill=random_color())


def random_color():
    '''
    Возвращает случайный цвет из некоторого набора цветов
    :return:
    '''
    return choice(ball_available_colors)

def init_ball_cathc_game():
    '''
    Создает необходимое для игры количество шариков, по которым нужно будет кликать
    '''
    for i in range(ball_initial_number):
        create_random_ball()


def init_main_window():
    global root, canvas

    root = Tk()
    canvas = Canvas(root, bg='white', width=400, height=400)
    canvas.bind('<Button>', click_ball)
    canvas.bind('<Motion>', move_all_balls)
    canvas.pack()


if __name__ == '__main__':
    init_main_window()
    init_ball_cathc_game()
    root.mainloop()
    print('Приходите поиграть еще!')
