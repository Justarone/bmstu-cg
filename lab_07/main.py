import time
import numpy as np
import tkinter as tk
from tkinter import colorchooser
from config import Point
import config as cfg
import tkinter.messagebox as mb


rect_color = cfg.DEFAULT_COLOUR
sect_color = cfg.DEFAULT_COLOUR
res_color = cfg.DEFAULT_COLOUR
left_corner = [None, None]
rect = [None, None, None, None]
sections = []
last_point = [None, None]

def clear_all():
    clear_canvas() 
    rect[cfg.LEFT] = None
    left_corner[0] = None
    sections.clear()
    last_point[0] = None

def erase_inside():
    canvas.create_rectangle(rect[cfg.LEFT], rect[cfg.TOP], rect[cfg.RIGHT], rect[cfg.BOTTOM],
                            fill=cfg.CANVAS_COLOUR, outline=rect_color)

def clear_canvas():
    canvas.delete('all')

def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)

def left_click(event):
    if last_point[0]:
        sections.append([last_point[:], [event.x, event.y]])
        draw_section(*sections[-1][0], *sections[-1][1], sect_color)
        last_point[0] = None
    else:
        last_point[0], last_point[1] = event.x, event.y


def return_click(event):
    erase_inside()
    solve()


def right_click(event):
    if not left_corner[0]:
        left_corner[0], left_corner[1] = event.x, event.y
    else:
        new_rect(left_corner[0], event.y, event.x, left_corner[1])


def draw_rect():
    canvas.create_line(rect[cfg.LEFT], rect[cfg.TOP], rect[cfg.RIGHT], rect[cfg.TOP], fill=rect_color)
    canvas.create_line(rect[cfg.RIGHT], rect[cfg.TOP], rect[cfg.RIGHT], rect[cfg.BOTTOM], fill=rect_color)
    canvas.create_line(rect[cfg.RIGHT], rect[cfg.BOTTOM], rect[cfg.LEFT], rect[cfg.BOTTOM], fill=rect_color)
    canvas.create_line(rect[cfg.LEFT], rect[cfg.BOTTOM], rect[cfg.LEFT], rect[cfg.TOP], fill=rect_color)


def draw_section(xb, yb, xe, ye, color):
    canvas.create_line(xb, yb, xe, ye, fill=color)


def new_rect(left, top, right, bottom):
    rect[cfg.LEFT] = left
    rect[cfg.TOP] = top
    rect[cfg.RIGHT] = right
    rect[cfg.BOTTOM] = bottom

    clear_canvas()
    draw_rect()
    sections.clear()
    left_corner[0] = None
    last_point[0] = None


def read_rect():
    new_rect(int(rect_left_entry.get()), int(rect_up_entry.get()),
             int(rect_right_entry.get()), int(rect_down_entry.get()))


def read_vertex():
    if last_point[0]:
        sections.append([last_point[:], [int(x_entry.get()), int(y_entry.get())]])
        draw_section(*sections[-1][0], *sections[-1][1], sect_color)
        last_point[0] = None
    else:
        last_point[0], last_point[1] = int(x_entry.get()), int(y_entry.get())


def change_rect_color():
    global rect_color
    rect_color = colorchooser.askcolor(title="select color")[1]
    rect_color_btn.configure(background=rect_color)


def change_sect_color():
    global sect_color
    sect_color = colorchooser.askcolor(title="select color")[1]
    sect_color_btn.configure(background=sect_color)

def change_res_color():
    global res_color
    res_color = colorchooser.askcolor(title="select color")[1]
    res_color_btn.configure(background=res_color)


def get_time():
    start_time = time.time()
    solve()
    mb.showinfo("Время.", f"Время построения: {time.time() - start_time: 8.7f}")


def solve():
    for section in sections:
        cut_section(rect, section)


MASK_LEFT =   0b0001
MASK_RIGHT =  0b0010
MASK_BOTTOM = 0b0100
MASK_TOP =    0b1000
def set_bits(point, rect_sides):
    bits = 0b0000
    if point[0] < rect_sides[cfg.LEFT]:
        bits += MASK_LEFT
    if point[0] > rect_sides[cfg.RIGHT]:
        bits += MASK_RIGHT
    if point[1] < rect_sides[cfg.BOTTOM]:
        bits += MASK_BOTTOM
    if point[1] > rect_sides[cfg.TOP]:
        bits += MASK_TOP
    return bits


def find_vertical(p, index, rect):
    if p[index][1] > rect[cfg.TOP]:
        return [p[index][0], rect[cfg.TOP]]
    elif p[index][1] < rect[cfg.BOTTOM]:
        return [p[index][0], rect[cfg.BOTTOM]]
    else:
        return p[index]


def cut_section(rect, p):
    s = list()
    for i in range(2):
        s.append(set_bits(p[i], rect))

    # Полностью видимый отрезок
    if s[0] == 0 and s[1] == 0:
        draw_section(p[0][0], p[0][1], p[1][0], p[1][1], res_color)
        return

    # Полностью невидимый отрезок
    if s[0] & s[1]:
        return

    # cur_index - содержит индекс текущей обрабатываемой вершины
    cur_index = 0
    res = list()

    # Проверка, нет ли одной точки внутри отсекателя (первая проверка для точки с индексом 0,
    # вторая - с индексом 1). Если вторая точка внутри области - поставим ее на первое место 
    # и работаем с другой (смена мест нужна, чтобы в начале была обработанная точка, а за ней - нет)
    if s[0] == 0:
        cur_index = 1
        res.append(p[0])

    elif s[1] == 0:
        res.append(p[1])
        cur_index = 1
        # Вторая вершина уже внутри области, поменяем местами вершины, чтобы работать с необработанной
        # на 2 месте
        p.reverse()
        s.reverse()

    while cur_index < 2:
        if p[0][0] == p[1][0]:
            res.append(find_vertical(p, cur_index, rect))
            cur_index += 1
            continue

        m = (p[1][1] - p[0][1]) / (p[1][0] - p[0][0])

        # Нахождение пересечения с левой границей
        if s[cur_index] & MASK_LEFT:
            y = round(m * (rect[cfg.LEFT] - p[cur_index][0]) + p[cur_index][1])
            if y <= rect[cfg.TOP] and y >= rect[cfg.BOTTOM]:
                res.append([rect[cfg.LEFT], y])
                cur_index += 1
                continue

        # Нахождение пересечения с правой границей
        elif s[cur_index] & MASK_RIGHT:
            y = round(m * (rect[cfg.RIGHT] - p[cur_index][0]) + p[cur_index][1])
            if y <= rect[cfg.TOP] and y >= rect[cfg.BOTTOM]:
                res.append([rect[cfg.RIGHT], y])
                cur_index += 1
                continue

        # Если прямая горизонтальна, пересечения с верхней и нижней границей быть не может
        # (заканчиваем обработку текущей вершины)
        if m == 0:
            cur_index += 1
            continue

        # Нахождение пересечений с верхней и нижней границами

        # С верхней (если рассматриваемая вершина выше верхней границы)
        if s[cur_index] & MASK_TOP:
            x = round((rect[cfg.TOP] - p[cur_index][1]) / m + p[cur_index][0])
            if x <= rect[cfg.RIGHT] and x >= rect[cfg.LEFT]:
                res.append([x, rect[cfg.TOP]])
                cur_index += 1
                continue

        # С нижней (если рассматриваемая вершина ниже нижней границы)
        elif s[cur_index] & MASK_BOTTOM:
            x = round((rect[cfg.BOTTOM] - p[cur_index][1]) / m + p[cur_index][0])
            if x <= rect[cfg.RIGHT] and x >= rect[cfg.LEFT]:
                res.append([x, rect[cfg.BOTTOM]])
                cur_index += 1
                continue

        cur_index += 1

    if res:
        draw_section(res[0][0], res[0][1], res[1][0], res[1][1], res_color)




root = tk.Tk()
root.title("Computer graphics 7 lab.")
root["bg"] = cfg.MAIN_COLOUR

data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

rect_color_label = tk.Label(data_frame, text="Цвет регулярного отсекателя", font=("Consolas", 14),
                            bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
sect_color_label = tk.Label(data_frame, text="Цвет отрезков", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                            fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
res_color_label = tk.Label(data_frame, text="Цвет результата", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                           fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rect_label = tk.Label(data_frame, text="Ввод границ отсекателя", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rect_left_label = tk.Label(data_frame, text="Левая", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rect_right_label = tk.Label(data_frame, text="Правая", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rect_up_label = tk.Label(data_frame, text="Верхняя", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rect_down_label = tk.Label(data_frame, text="Нижняя", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
vertex_label = tk.Label(data_frame, text="Ввод вершины", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
x_label = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
y_label = tk.Label(data_frame, text="y", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


rect_left_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_right_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_up_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_down_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")


rect_btn = tk.Button(data_frame, text="Применить", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=read_rect,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
vertex_btn = tk.Button(data_frame, text="Применить", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=read_vertex,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
solve_btn = tk.Button(data_frame, text="Отсечь", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=solve,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
info_btn = tk.Button(data_frame, text="Информация", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
rect_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14),
                           bg=cfg.DEFAULT_COLOUR, fg=cfg.ADD_COLOUR, command=change_rect_color,
                           relief=tk.GROOVE)
sect_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14),
                           bg=cfg.DEFAULT_COLOUR, fg=cfg.ADD_COLOUR, command=change_sect_color,
                           relief=tk.GROOVE)
res_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14),
                          bg=cfg.DEFAULT_COLOUR, fg=cfg.ADD_COLOUR, command=change_res_color,
                          relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_all,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0

rect_color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
rect_color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1


sect_color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
sect_color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

res_color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
res_color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

rect_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
rect_left_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
rect_right_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
rect_left_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
rect_right_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)

offset += 1
rect_up_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
rect_down_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
rect_up_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
rect_down_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
rect_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

vertex_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1
x_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
x_entry.place(x=1 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
              height=cfg.SLOT_HEIGHT)
y_label.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
              height=cfg.SLOT_HEIGHT)
y_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
              height=cfg.SLOT_HEIGHT)
offset += 1
vertex_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)


offset = cfg.ROWS - 3

solve_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

info_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
               width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)


canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.bind("<Button-1>", left_click)
root.bind("<Return>", return_click)
canvas.bind("<Button-3>", right_click)

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')

root.mainloop()
