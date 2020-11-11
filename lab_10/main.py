import tkinter as tk
from math import pi, cos, sin
from tkinter import colorchooser
import config as cfg
import tkinter.messagebox as mb
from copy import deepcopy
from functions import funcs
from numpy import arange

color = cfg.DEFAULT_COLOUR

sf = 48
x_from = -10
x_to = 10
x_step = 0.1

z_from = -10
z_to = 10
z_step = 0.1

trans_matrix = [[int(i == j) for i in range(4)] for j in range(4)]


def clear_all():
    clear_canvas()


def clear_canvas():
    canvas.delete('all')


def change_color():
    global color, color_btn
    color = colorchooser.askcolor(title="select color")[1]
    color_btn.configure(background=color)


def draw_section(xb, yb, xe, ye, color):
    canvas.create_line(xb, yb, xe, ye, fill=color)


def rotate_trans_matrix(rotate_matrix):
    global trans_matrix
    res_matrix = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                res_matrix[i][j] += trans_matrix[i][k] * rotate_matrix[k][j]

    trans_matrix = res_matrix


def trans_point(point):
    # point = (x, y, z)
    point.append(1) # (x, y, z, 1)
    res_point = [0, 0, 0, 0]
    for i in range(4):
        for j in range(4):
            res_point[i] += point[j] * trans_matrix[j][i]

    for i in range(3):
        res_point[i] *= sf # x, y, z ==> SF * x, SF * y, SF * z

    res_point[0] += cfg.FIELD_WIDTH / 2
    res_point[1] += cfg.FIELD_HEIGHT / 2

    return res_point[:3]


def rotate_x():
    value = float(x_entry.get()) / 180 * pi
    rotate_matrix = [ [ 1, 0, 0, 0 ],
                       [ 0, cos(value), sin(value), 0 ],
                       [ 0, -sin(value), cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_y():
    value = float(y_entry.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), 0, -sin(value), 0 ],
                       [ 0, 1, 0, 0 ],
                       [ sin(value), 0, cos(value), 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def rotate_z():
    value = float(z_entry.get()) / 180 * pi
    rotate_matrix = [ [ cos(value), sin(value), 0, 0 ],
                       [ -sin(value), cos(value), 0, 0 ],
                       [ 0, 0, 1, 0 ],
                       [ 0, 0, 0, 1 ] ]
    rotate_trans_matrix(rotate_matrix)
    solve()


def set_sf():
    global sf
    sf = float(scale_entry.get())
    solve()

def set_meta():
    global x_from, x_step, x_to, z_from, z_step, z_to
    x_from = float(xfrom_entry.get())
    x_to = float(xto_entry.get())
    x_step = float(xstep_entry.get())
    z_from = float(zfrom_entry.get())
    z_to = float(zto_entry.get())
    z_step = float(zstep_entry.get())
    solve()


def draw_pixel(x, y):
    canvas.create_line(x, y, x + 1, y + 1, fill=color)


def is_visible(point):
    return 0 <= point[0] < cfg.FIELD_WIDTH and 0 <= point[1] < cfg.FIELD_HEIGHT


def draw_point(x, y, hh, lh):
    if not is_visible([x, y]):
        return False

    if y > hh[x]:
        hh[x] = y
        draw_pixel(x, y)

    elif y < lh[x]:
        lh[x] = y
        draw_pixel(x, y)

    return True


def draw_horizon_part(p1, p2, hh, lh):
    if p1[0] > p2[0]: # хочу, чтобы x2 > x1
        p1, p2 = p2, p1

    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    l = dx if dx > dy else dy
    dx /= l
    dy /= l

    x, y = p1[0], p1[1]

    for _ in range(int(l) + 1):
        if not draw_point(int(round(x)), y, hh, lh):
            return
        x += dx
        y += dy


def draw_horizon(func, hh, lh, fr, to, step, z):
    f = lambda x: func(x, z) # f = f(x, z=const)
    prev = None
    for x in arange(fr, to + step, step):
        # x, z, f(x, z=const)
        current = trans_point([x, f(x), z]) # transformed: Повернуть, масштабировать и сдвинуть в центр экрана
        if prev: # Если это не первая точка (то есть если есть предыдущая)
            draw_horizon_part(prev, current, hh, lh)
        prev = current


def solve():
    clear_canvas()
    f = funcs[func_var.get()]
    high_horizon = [0 for i in range(cfg.FIELD_WIDTH)]
    low_horizon = [cfg.FIELD_HEIGHT for i in range(cfg.FIELD_WIDTH)]

    for z in arange(z_from, z_to + z_step, z_step):
        draw_horizon(f, high_horizon, low_horizon, x_from, x_to, x_step, z)

    for z in arange(z_from, z_to, z_step):
        p1 = trans_point([x_from, f(x_from, z), z])
        p2 = trans_point([x_from, f(x_from, z + z_step), z + z_step])
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)
        p1 = trans_point([x_to, f(x_to, z), z])
        p2 = trans_point([x_to, f(x_to, z + z_step), z + z_step])
        canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill=color)
        


# ==================================================================
# ==================================================================
# ===================== GUI PART STARTS HERE =======================
# ==================================================================
# ==================================================================

root = tk.Tk()
root.title("Computer graphics 10 lab.")
root["bg"] = cfg.MAIN_COLOUR

data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

func_var = tk.IntVar()
func_var.set(0)
func_radios = list()
for i in range(len(cfg.FUNCS)):
    func_radios.append(tk.Radiobutton(data_frame, text=cfg.FUNCS[i], bg=cfg.ADD_COLOUR,
                                      fg=cfg.MAIN_COLOUR, variable=func_var, value=i))

color_label = tk.Label(data_frame, text="Цвет", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                       fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
rotate_label = tk.Label(data_frame, text="Вращение", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
meta_label = tk.Label(data_frame, text="Пределы и шаг", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
x_label = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
y_label = tk.Label(data_frame, text="y", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
z_label = tk.Label(data_frame, text="z", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
xlabel = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
zlabel = tk.Label(data_frame, text="z", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                   fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
from_label = tk.Label(data_frame, text="От", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
to_label = tk.Label(data_frame, text="До", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                    fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
step_label = tk.Label(data_frame, text="Шаг", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
func_label = tk.Label(data_frame, text="Функция", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
scale_label = tk.Label(data_frame, text="Коэффициент\nмасштабирования",
                       font=("Consolas", 11), bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
z_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")

x_entry.insert(0, "20")
y_entry.insert(0, "20")
z_entry.insert(0, "20")

xfrom_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")
xto_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                    fg=cfg.MAIN_COLOUR, justify="center")
xstep_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")

xfrom_entry.insert(0, str(x_from))
xto_entry.insert(0, str(x_to))
xstep_entry.insert(0, str(x_step))

zfrom_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")
zto_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                    fg=cfg.MAIN_COLOUR, justify="center")
zstep_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")

zfrom_entry.insert(0, str(z_from))
zto_entry.insert(0, str(z_to))
zstep_entry.insert(0, str(z_step))

scale_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                      fg=cfg.MAIN_COLOUR, justify="center")
scale_entry.insert(0, str(sf))


x_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_x,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
y_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_y,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
z_btn = tk.Button(data_frame, text="Вращать", font=("Consolas", 14),
                  bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_z,
                  activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
confirm_btn = tk.Button(data_frame, text="Применить", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=set_meta,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
scale_button = tk.Button(data_frame, text="Изменить", font=("Consolas", 14),
                         bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=set_sf,
                         activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

res_btn = tk.Button(data_frame, text="Нарисовать", font=("Consolas", 14),
                    bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=solve,
                    activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
color_btn = tk.Button(data_frame, text="", font=("Consolas", 14), bg=color,
                      command=change_color, relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_all,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0

color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                  height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1

color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

func_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH,
                 height=cfg.SLOT_HEIGHT)

for i in range(len(func_radios)):
    offset += 1
    func_radios[i].place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH,
                     height=cfg.SLOT_HEIGHT)
offset += 2

meta_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

from_label.place(x=cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
to_label.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
               height=cfg.SLOT_HEIGHT)
step_label.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
                 height=cfg.SLOT_HEIGHT)
offset += 1

xlabel.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
xfrom_entry.place(x=cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
xto_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
               height=cfg.SLOT_HEIGHT)
xstep_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
                 height=cfg.SLOT_HEIGHT)
offset += 1

zlabel.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
zfrom_entry.place(x=cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 4, height=cfg.SLOT_HEIGHT)
zto_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
               height=cfg.SLOT_HEIGHT)
zstep_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 4,
                 height=cfg.SLOT_HEIGHT)
offset += 1

confirm_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                  width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

scale_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
scale_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
scale_button.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)

rotate_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                   width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

x_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
x_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
x_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)
offset += 1

y_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
y_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
y_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)
offset += 1

z_label.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 3, height=cfg.SLOT_HEIGHT)
z_entry.place(x=cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
              height=cfg.SLOT_HEIGHT)
z_btn.place(x=2 * cfg.DATA_WIDTH // 3, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 3,
            height=cfg.SLOT_HEIGHT)

offset = cfg.ROWS - 2

res_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
root.bind("<Return>", lambda x: solve())

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')

root.mainloop()
