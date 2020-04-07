from math import pi, cos, sin, sqrt, radians
import time
import tkinter as tk
from tkinter import colorchooser
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

draw_color = cfg.DEFAULT_COLOUR

vertex = []
extrems = []
mark_list = list()

pmax = Point()
pmin = Point(cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT)


def reset():
    mark_list.clear()
    vertex.clear()
    extrems.clear()
    pmax.x, pmax.y = 0, 0
    pmin.x, pmin.y = cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT
    img.put("#FFFFFF", to=(0, 0, cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT))


def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


def draw_pixel(p: Point):
    img.put(p.colour, (p.x, p.y))


def draw_section(section):
    for p in section:
        draw_pixel(p)



def update_max_area(event):
    if event.x > pmax.x:
        pmax.x = event.x
    if event.x < pmin.x:
        pmin.x = event.x
    if event.y > pmax.y:
        pmax.y = event.y
    if event.y < pmin.y:
        pmin.y = event.y


def left_click(event):
    update_max_area(event)
    vertex.append(Point(event.x, event.y, draw_color))
    if len(vertex) > 1:
        section = brezenham_int(draw_color, vertex[-2].x, vertex[-2].y, 
                                vertex[-1].x, vertex[-1].y)

        if len(vertex) > 2:
            if vertex[-2].y < vertex[-1].y and vertex[-2].y < vertex[-3].y or \
                    vertex[-2].y > vertex[-1].y and vertex[-2].y > vertex[-3].y:
                extrems.append(len(vertex) - 2)

        draw_section(section)


def right_click(event):
    if len(vertex) > 1:
        for i in range(-1, 1):
            if vertex[i].y < vertex[i - 1].y and vertex[i].y < vertex[i + 1].y or \
                    vertex[i].y > vertex[i - 1].y and vertex[i].y > vertex[i + 1].y:
                extrems.append(i)

        section = brezenham_int(draw_color, vertex[-1].x, vertex[-1].y,
                                      vertex[0].x, vertex[0].y)
        draw_section(section)

        for i in range(len(vertex)):
            xb = vertex[i].x
            yb = vertex[i].y
            xe = vertex[(i + 1) % len(vertex)].x
            ye = vertex[(i + 1) % len(vertex)].y
            add_list = brezenham_int(draw_color, xb, yb, xe, ye, True)
            print(extrems)
            if i in extrems:
                prep_list(add_list)
            if (i + 1) % len(add_list) in extrems:
                prep_list(add_list, last=True)

            mark_list.extend(add_list)

        # vertex.clear()
        # extrems.clear()


def prep_list(add_list, last=False):
    index = 0 if not last else len(add_list) - 1
    add_list.pop(index)


def brezenham_int(colour, xb, yb, xe, ye, mark=False):
    section = list()
    mark_list = list()
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
            if not mark:
                section.append(Point(x, y, colour))

            if e >= 0:
                if mark:
                    mark_list.append((x, y))
                y += sy
                e -= dx + dx
            x += sx
            e += dy + dy
    else:
        for _ in range(dx):
            if mark:
                mark_list.append((x, y))
            else:
                section.append(Point(x, y, colour))

            if e >= 0:
                x += sx
                e -= dx + dx
            y += sy
            e += dy + dy

    return section if not mark else mark_list


def change_color():
    global draw_color
    draw_color = colorchooser.askcolor(title="select color")[1]
    colour_btn.configure(background=draw_color)


def get_time():
    pass


def solve():
    global pmax, pmin
    print("START MARK")
    print("START FILL")


    # img.put("#FFFFFF", (0, 0, cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT))
    # for i in range(len(mark_list)):
        # img.put("#FF0000", mark_list[i])
    # for i in range(len(extrems)):
        # img.put("#0000FF", (vertex[extrems[i]].x, vertex[extrems[i]].y))

    # mark_list = mark_part()
    fill_part(mark_list)
    print('DONE')
    vertex.clear()
    extrems.clear()
    pmax.x, pmax.y = 0, 0
    pmin.x, pmin.y = cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT


def toggle_color(color):
    return draw_color if color != draw_color else cfg.CANVAS_COLOUR


def fill_part(mark_list):
    cur_color = cfg.CANVAS_COLOUR
    for y in range(pmax.y, pmin.y, -1):
        for x in range(pmin.x, pmax.x + 1):
            if (x, y) in mark_list:
                cur_color = toggle_color(cur_color)
            draw_pixel(Point(x, y, cur_color))



root = tk.Tk()
root.title("Computer graphics 5 lab.")
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
mode = tk.IntVar()
mode.set(0)
mode_radios = list()
for i in range(len(cfg.MODES)):
    mode_radios.append(tk.Radiobutton(data_frame, text=cfg.MODES[i], bg=cfg.ADD_COLOUR,
                                        fg=cfg.MAIN_COLOUR, variable=mode, value=i))
# index = list(points_listbox.curselection())


modes_label = tk.Label(data_frame, text="Режимы", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                       fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

colour_label = tk.Label(data_frame, text="Цвет", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


solve_btn = tk.Button(data_frame, text="Закрасить", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=solve,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
time_btn = tk.Button(data_frame, text="Сравнить время", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=get_time,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
info_btn = tk.Button(data_frame, text="Информация", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
colour_btn = tk.Button(data_frame, text="", font=("Consolas", 14),
                       bg=cfg.DEFAULT_COLOUR, fg=cfg.ADD_COLOUR, command=change_color,
                       relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=reset,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0
modes_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                   height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
for i in range(len(mode_radios)):
    mode_radios[i].place(x=0, y=cfg.SLOT_HEIGHT * offset + i * cfg.SLOT_HEIGHT,
                         width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 3

colour_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                   height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1

colour_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset = cfg.ROWS - 4


solve_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

time_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

info_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)


canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-3>", right_click)

img = tk.PhotoImage(width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)
canvas.create_image((cfg.FIELD_WIDTH // 2, cfg.FIELD_HEIGHT // 2), image=img, state='normal')
reset()

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)


print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')


root.mainloop()
