from math import pi, cos, sin, sqrt
import time
import tkinter as tk
from config import Colour, Point
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


def cda(colour, xb, yb, xe, ye):
    section = list()
    dx, dy = xe - xb, ye - yb
    delta_x, delta_y = abs(dx), abs(dy)
    l = delta_x if delta_x > delta_y else delta_y
    dx /= l
    dy /= l
    x, y = xb, yb
    for _ in range(l):
        section.append(Point(int(x), int(y), colour))
        x += dx
        y += dy
    return section


def brezenham_float(colour, xb, yb, xe, ye):
    section = list()

    x, y = xb, yb
    dx = xe - xb
    dy = ye - yb

    sx = int(np.sign(dx))
    sy = int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        dx, dy = dy, dx

    m = dy / dx
    e = m - 1 / 2

    if not obmen:
        for _ in range(dx):
            section.append(Point(int(x), int(y), colour))

            if e >= 0:
                y += sy
                e -= 1
            x += sx
            e += m
    else:
        for _ in range(dx):
            section.append(Point(int(x), int(y), colour))

            if e >= 0:
                x += sx
                e -= 1
            y += sy
            e += m

    return section


def brezenham_int(colour, xb: int, yb: int, xe: int, ye: int):
    section = list()
    x, y = xb, yb
    dx = xe - xb
    dy = ye - yb
    sx = int(np.sign(dx))
    sy = int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        dx, dy = dy, dx

    e = dy + dy - dx

    if not obmen:
        for _ in range(dx):
            section.append(Point(x, y, colour))

            if e >= 0:
                y += sy
                e -= dx + dx
            x += sx
            e += dy + dy
    else:
        for _ in range(dx):
            section.append(Point(x, y, colour))

            if e >= 0:
                x += sx
                e -= dx + dx
            y += sy
            e += dy + dy

    return section


def brezenham_double(colour, xb, yb, xe, ye):
    section = list()
    x, y = xb, yb
    dx = xe - xb
    dy = ye - yb
    sx = int(np.sign(dx))
    sy = int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        dx, dy = dy, dx

    m = dy / dx
    e = 1 / 2
    w = 1

    if not obmen:
        for _ in range(dx):
            section.append(Point(int(x), int(y), 
                                 colour.intensity_apply(1 - e)))
            section.append(Point(int(x), int(y + sy), 
                                 colour.intensity_apply(e)))
            if e >= w - m:
                y += sy
                e -= w
            x += sx
            e += m
    else:
        for _ in range(dx):
            section.append(Point(int(x), int(y), 
                                 colour.intensity_apply(1 - e)))
            section.append(Point(int(x + sx), int(y), 
                                 colour.intensity_apply(e)))
            if e >= w - m:
                x += sx
                e -= w
            y += sy
            e += m

    return section


def vu(colour: Colour, xb, yb, xe, ye):
    section = list()
    x, y = xb, yb
    dx = xe - xb
    dy = ye - yb
    sx = 1 if dx == 0 else int(np.sign(dx))
    sy = 1 if dy == 0 else int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        dx, dy = dy, dx

    m = dy / dx
    e = -1

    if not obmen:
        for _ in range(dx):
            section.append(Point(int(x), int(y), 
                                 colour.intensity_apply(-e)))
            section.append(Point(int(x), int(y + sy), 
                                 colour.intensity_apply(1 + e)))

            e += m
            if e >= 0:
                y += sy
                e -= 1
            x += sx
    else:
        for _ in range(dx):
            section.append(Point(int(x), int(y), 
                                 colour.intensity_apply(-e)))
            section.append(Point(int(x + sx), int(y), 
                                 colour.intensity_apply(1 + e)))

            e += m
            if e >= 0:
                x += sx
                e -= 1
            y += sy

    return section


def library(colour, xb, yb, xe, ye):
    canvas.create_line(xb, yb, xe, ye, fill=str(colour))
    return list()


def clear_canvas():
    global canvas
    canvas.delete("all")


def create_beam():
    try:
        r = int(r_entry.get())
        angle = int(alpha_entry.get())
        if angle >= 360 or angle <= 0 or r <= 0:
            raise ArithmeticError
    except ValueError:
        mb.showerror("Неверный формат.", "Введите натуральные числа в поля ввода.")
    except ArithmeticError:
        mb.showerror("Неверный формат.", "Введите корректное значение угла (0 < angle < 360).")

    colour_index = colour.get()
    method_index = method.get()

    global sections

    xb, yb = cfg.CANVAS_CENTER[0], cfg.CANVAS_CENTER[1]
    times[method_index] = 0
    for t in np.arange(0, 2 * pi, pi * angle / 180):
        xe, ye = int(xb + r * cos(t)), int(yb - r * sin(t))
        start_time = time.time()
        sections[method_index] = methods[method_index](cfg.COLOURS_CODES[colour_index],
                                                       xb, yb, xe, ye)
        times[method_index] += (time.time() - start_time) / cfg.COEFFS[method_index]
        draw_section(sections[method_index])


def compare_methods():
    to_show_list = list()
    for i in range(len(times)):
        if times[i] != -1:
            to_show_list.append(i)
    if not to_show_list:
        mb.showerror("Нет замеров.", "Пока еще не было замеров времени, повторите операцию позже." \
                     "\n(учтите, что замеры производятся только при построении пучков!)")
        return

    objects = [cfg.METHODS[i] for i in to_show_list]
    performance = [times[i] for i in to_show_list]

    y_pos = np.arange(len(to_show_list))
    plt.bar(y_pos, performance, align='center', alpha=0.5)
    plt.xticks(y_pos, objects)
    plt.ylabel("Time")
    plt.xlabel("Method")
    plt.title("Time of drawing section with methods.")

    plt.show()


def process_section():
    try:
        xb, yb = int(x1_entry.get()), int(y1_entry.get())
        xe, ye = int(x2_entry.get()), int(y2_entry.get())
    except:
        mb.showerror("Ошибка ввода", "Введите целые числа в поля ввода")

    colour_index = colour.get()
    method_index = method.get()

    global sections

    sections[method_index] = methods[method_index](cfg.COLOURS_CODES[colour_index], xb, yb, xe, ye)
    draw_section(sections[method_index])


def draw_section(section):
    for p in section:
        draw_pixel(p)
    

def draw_pixel(p: Point):
    canvas.create_line(p.x, p.y, p.x, p.y, fill=str(p.colour))


# if __name__ == "__main__":
times = [-1 for i in range(6)]
sections = [list() for i in range(cfg.NOM)]
methods = [cda, brezenham_int, brezenham_float, brezenham_double, vu, library]

root = tk.Tk()
root.title("Computer graphics 3 lab.")
root["bg"] = cfg.MAIN_COLOUR
root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)


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


x1_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y1_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
x2_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y2_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
r_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
alpha_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")

solve_label = tk.Label(data_frame, text="Координаты точки\n((Xн, Ун), (Xк, Ук)).", 
                       font=("Consolas", 12), bg=cfg.MAIN_COLOUR,
                       fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

colour_label = tk.Label(data_frame, text="Цвет", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

method_label = tk.Label(data_frame, text="Метод", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

beam_label = tk.Label(data_frame, text="Пучок\n(радиус ,  угол)", font=("Consolas", 13),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


solve_btn = tk.Button(data_frame, text="Построить отрезок", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=process_section,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
compare_btn = tk.Button(data_frame, text="Cравнить методы", font=("Consolas", 14),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=compare_methods,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
beam_btn = tk.Button(data_frame, text="Построить пучок", font=("Consolas", 14),
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
solve_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                  height=2 * cfg.DATA_HEIGHT // cfg.ROWS)
offset += 2
x1_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 4,
               height=cfg.DATA_HEIGHT // cfg.ROWS)
y1_entry.place(x=cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
x2_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
y2_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
solve_btn.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
beam_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                 height=2 * cfg.DATA_HEIGHT // cfg.ROWS)
offset += 2
r_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                 height=cfg.DATA_HEIGHT // cfg.ROWS)
alpha_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                  width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.ROWS)
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
