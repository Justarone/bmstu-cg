from math import pi, cos, sin, sqrt, radians
import time
import tkinter as tk
from config import Point
import config as cfg
import tkinter.messagebox as mb
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке (применяется при наведении на окно root)
# entry.get()
# label['text'] = ''
# root.bind("<Return>", lambda x: find_solution())

def dup_x(points, x, y):
    points += list(map(lambda p: Point(p.x, 2 * y - p.y, p.colour), points))

def dup_y(points, x, y):
    points += list(map(lambda p: Point(2 * x - p.x, p.y, p.colour), points))

def dup_biss(points, x, y):
    points += list(map(lambda p: Point(x + p.y - y, y + p.x - x, p.colour), points))
    

def normal_c(x, y, r, colour):
    points = list()
    R = r * r
    for a in range(x, round(x + r / sqrt(2)) + 1):
        b = y + sqrt(R - (a - x) * (a - x))
        points.append(Point(a, b, colour))

    dup_biss(points, x, y)
    dup_x(points, x, y)
    dup_y(points, x, y)

    return points


def param_c(x, y, r, colour):
    points = list()
    step = 1 / r
    for t in np.arange(0, pi / 4 + step, step):
        a = x + r * cos(t)
        b = y + r * sin(t)
        points.append(Point(a, b, colour))

    dup_biss(points, x, y)
    dup_x(points, x, y)
    dup_y(points, x, y)

    return points


def brezenham_c(xc, yc, r, colour):
    points = list()
    x = xc
    y = yc + r
    ye = yc

    while y > ye:
        points.append(Point(x, y, colour))



    
    dup_x(points, xc, yc)
    dup_y(points, xc, yc)

    return points


def middle_point_c(xc, yc, r, colour):

    points = list()
    x = r
    y = 0
    
    points.append(Point(xc + x, yc + y, colour))
    p = 1 - r  

    while x > y:
        y += 1

        if (p <= 0):  
            p += y + y + 3
              
        else:          
            x -= 1
            p += y + y - x - x + 5
          
        points.append(Point(xc + x, yc + y, colour))
    
    dup_biss(points, xc, yc)
    dup_x(points, xc, yc)
    dup_y(points, xc, yc)

    return points


def library_c(x, y, r, colour):
    canvas.create_oval(x - r, y - r, x + r, y + r, outline=colour, width=1)
    return []


def normal_o(x, y, r1, r2, colour):
    points = list()
    R = r1 * r1 * r2 * r2

    limit1 = round(x + r1 / sqrt(1 + r2 * r2 / r1 / r1))

    for a in range(x, limit1):
        b = y + sqrt(R - (a - x) * (a - x) * r2 * r2) / r1
        points.append(Point(a, b, colour))

    limit2 = round(y + r2 / sqrt(1 + r1 * r1 / r2 / r2))

    for b in range(limit2, y - 1, -1):
        a = x + sqrt(R - (b - y) * (b - y) * r1 * r1) / r2
        points.append(Point(a, b, colour))

    dup_x(points, x, y)
    dup_y(points, x, y)

    return points


def param_o(x, y, r1, r2, colour):
    points = list()
    step = 1 / r1 if r1 > r2 else 1 / r2
    for t in np.arange(0, pi / 2 + step, step):
        a = x + r1 * cos(t)
        b = y + r2 * sin(t)
        points.append(Point(a, b, colour))

    dup_x(points, x, y)
    dup_y(points, x, y)

    return points


def brezenham_o(x, y, r1, r2, colour):
    return list()


def middle_point_o(x, y, r1, r2, colour):
    return list()


def library_o(x, y, r1, r2, colour):
    canvas.create_oval(x - r1, y - r2, x + r1, y + r2, outline=colour, width=1)
    return []


def clear_canvas():
    global canvas
    canvas.delete("all")


def process_input_c(rs, re, step, num):
    if rs == None:
        if re == None or step == None or num == None:
            re, rs, step, num = None, None, None, None
        else:
            rs = re - step * (num - 1)

    elif re == None:
        if rs == None or step == None or num == None:
            re, rs, step, num = None, None, None, None
        else:
            re = rs + step * (num - 1)

    elif step == None:
        if re == None or rs == None or num == None:
            re, rs, step, num = None, None, None, None
        else:
            step = (re - rs) // (num - 1)

    elif num == None:
        if re == None or step == None or rs == None:
            re, rs, step, num = None, None, None, None
        else:
            num = 1 + (rs - re) // step

    rs, re, step, num = int(rs), int(re), int(step), int(num)
    return rs, re, step, num


def create_beam():
    try:
        xc = int(xc_entry.get())
        yc = int(yc_entry.get())
        rs = rs_entry.get()
        re = re_entry.get()
        step = step_entry.get()
        num = num_entry.get()
    except ValueError:
        mb.showerror("Ошибка ввода.", "В поля введены некорректные данные.")
        return

    figure_index = figure.get()
    colour_index = colour.get()
    method_index = method.get()

    if figure_index == cfg.CIRCLE:
        rs, re, step, num = process_input_c(rs, re, step, num)
        if rs == None:
            mb.showerror("Ошибка ввода.", "В поля введены некорректные данные.")
            return

        for cur_r in range(rs, re, step):
            points = methods[cfg.CIRCLE][method_index](xc, yc, cur_r, cfg.COLOURS_CODES[colour_index])
            draw_figure(points)

    else:
        try:
            rs = int(rs)
            re = int(re)
            step = int(step)
            num = int(num)
        except ValueError:
            mb.showerror("Ошибка ввода.", "В поля введены некорректные данные.")
            return

        cur_r = rs
        for _ in range(num):
            points = methods[cfg.OVAL][method_index](xc, yc, cur_r, re, cfg.COLOURS_CODES[colour_index])
            cur_r += step
            draw_figure(points)


    # for i in range(10):
        # start_time = time.time()
        # sections[method_index] = methods[method_index](cfg.COLOURS_CODES[colour_index],
                                                       # xb, yb, xe, ye)
        # times[method_index] += (time.time() - start_time) / cfg.COEFFS[method_index]
        # draw_section(sections[method_index])


def compare_methods():
    pass
    # to_show_list = list()
    # for i in range(len(times)):
        # if times[i] != -1:
            # to_show_list.append(i)
    # if not to_show_list:
        # mb.showerror("Нет замеров.", "Пока еще не было замеров времени, повторите операцию позже." \
                     # "\n(учтите, что замеры производятся только при построении пучков!)")
    # return


def process_figure():
    try:
        x, y = int(x_entry.get()), int(y_entry.get()) 
        r1 = int(r1_entry.get())
        r2 = r2_entry.get() 

    except ValueError:
        mb.showerror("Ошибка ввода", "Введите целые числа в поля ввода.")
        return 

    figure_index = figure.get()
    colour_index = colour.get()
    method_index = method.get()

    if figure_index == cfg.CIRCLE:
        if r1 <= 0:
            mb.showerror("Ошибка радиуса", "Радиус должен быть положительным")
            return
        points = methods[cfg.CIRCLE][method_index](x, y, r1, cfg.COLOURS_CODES[colour_index])
    else:
        try:
            r2 = int(r2)
        except ValueError:
            mb.showerror("Ошибка ввода", "Введите целые числа в поля ввода.")
            return
        if r1 <= 0 and r2 <= 0:
            mb.showerror("Ошибка радиуса", "Радиус должен быть положительным")
            return

        points = methods[cfg.OVAL][method_index](x, y, r1, r2, cfg.COLOURS_CODES[colour_index])

    draw_figure(points)


def draw_figure(figure):
    for p in figure:
        draw_pixel(p)
    

def draw_pixel(p: Point):
    canvas.create_line(p.x, p.y, p.x, p.y, fill=p.colour)


times = [[-1 for i in range(cfg.NOM)] for j in range(2)]
methods = [[normal_c, param_c, brezenham_c, middle_point_c, library_c], 
           [normal_o, param_o, brezenham_o, middle_point_o, library_o]]

root = tk.Tk()
root.title("Computer graphics 4 lab.")
root["bg"] = cfg.MAIN_COLOUR
# root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
# root.resizable(height=False, width=False)


data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

# For move command.
method = tk.IntVar()
method.set(0)
method_radios = list()
for i in range(len(cfg.METHODS)):
    method_radios.append(tk.Radiobutton(data_frame, text=cfg.METHODS[i], bg=cfg.ADD_COLOUR,
                                        fg=cfg.MAIN_COLOUR, variable=method, value=i))
# index = list(points_listbox.curselection())

colour = tk.IntVar()
colour.set(0)
colour_radios = list()
for i in range(len(cfg.COLOURS)):
    colour_radios.append(tk.Radiobutton(data_frame, text=cfg.COLOURS[i], bg=cfg.ADD_COLOUR, 
                                        fg=cfg.MAIN_COLOUR, variable=colour, value=i))

figure = tk.IntVar()
figure.set(0)
figure_radios = list()
figure_radios.append(tk.Radiobutton(data_frame, text="Окружность", bg=cfg.ADD_COLOUR, 
                                    fg=cfg.MAIN_COLOUR, variable=figure, value=0))
figure_radios.append(tk.Radiobutton(data_frame, text="Эллипс", bg=cfg.ADD_COLOUR, 
                                    fg=cfg.MAIN_COLOUR, variable=figure, value=1))

x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
r1_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
r2_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
xc_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
yc_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rs_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
re_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
step_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
num_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")

solve_label = tk.Label(data_frame, text="Параметры окружности (эллипса)\n((Xц, Уц), R1, R2)." \
                       + "\n(для окружности R2 игнорируется)",
                       font=("Consolas", 12), bg=cfg.MAIN_COLOUR,
                       fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

colour_label = tk.Label(data_frame, text="Цвет", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

method_label = tk.Label(data_frame, text="Метод", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

figure_label = tk.Label(data_frame, text="Фигура", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

beam_label = tk.Label(data_frame, text="Спектр (если все заполнено,\nполе \"кол-во\" " \
                      + "игнорируется)\n" \
                      + "[      Xц        |        Yц      ]\n [R1      |  R2     |" \
                      + "   шаг   |   кол-во]\n", font=("Consolas", 12), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


solve_btn = tk.Button(data_frame, text="Построить фигуру", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=process_figure,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
compare_btn = tk.Button(data_frame, text="Cравнить методы", font=("Consolas", 14),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=compare_methods,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
beam_btn = tk.Button(data_frame, text="Построить спектр", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=create_beam,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_canvas,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0
method_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                   height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
for i in range(len(method_radios)):
    method_radios[i].place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS + 5 * i * cfg.DATA_HEIGHT /
                           len(method_radios) // cfg.ROWS, width=cfg.DATA_WIDTH,
                           height=5 * cfg.DATA_HEIGHT / len(method_radios) // cfg.ROWS)
offset += 5
colour_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                   height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
for i in range(len(colour_radios)):
    colour_radios[i].place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS + 5 * i * cfg.DATA_HEIGHT /
                           len(colour_radios) // cfg.ROWS, width=cfg.DATA_WIDTH,
                           height=5 * cfg.DATA_HEIGHT / len(colour_radios) // cfg.ROWS)
offset += 5

figure_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                   height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
for i in range(len(figure_radios)):
    figure_radios[i].place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS +
                           5 * i * cfg.DATA_HEIGHT /
                           len(colour_radios) // cfg.ROWS, width=cfg.DATA_WIDTH,
                           height=5 * cfg.DATA_HEIGHT / len(colour_radios) // cfg.ROWS)
offset += 2

solve_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                  height=2 * cfg.DATA_HEIGHT // cfg.ROWS)
offset += 2

x_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 4,
               height=cfg.DATA_HEIGHT // cfg.ROWS)
y_entry.place(x=cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
r1_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
r2_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
solve_btn.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
beam_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                 height=3 * cfg.DATA_HEIGHT // cfg.ROWS)
offset += 3
xc_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)
yc_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                  width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1


rs_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 4,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)
re_entry.place(x=cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
step_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                 width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
num_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)

offset += 1


beam_btn.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
compare_btn.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
clear_btn.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)


canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)


print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')


root.mainloop()
