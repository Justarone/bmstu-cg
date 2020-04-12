import numpy as np
import time
import tkinter as tk
from tkinter import colorchooser
from config import Point
import config as cfg
import tkinter.messagebox as mb


draw_color = cfg.DEFAULT_COLOUR

vertex_list = [[]]
extrems = [[]]

def reset():
    global vertex_list, extrems
    vertex_list = [[]]
    extrems = [[]]


def reset_image():
    img.put("#FFFFFF", to=(0, 0, cfg.FIELD_WIDTH, cfg.FIELD_HEIGHT))


def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


def draw_section(section):
    for p in section:
        img.put(p.colour, (p.x, p.y))


def put_point():
    p = Point(int(x_entry.get()), int(y_entry.get()))
    left_click(p)

def left_click(event):
    vertex_list[-1].append(Point(event.x, event.y, draw_color))
    if len(vertex_list[-1]) > 1:
        section = brezenham_int(draw_color, vertex_list[-1][-2].x, vertex_list[-1][-2].y,
                                vertex_list[-1][-1].x, vertex_list[-1][-1].y)

        draw_section(section)


def right_click(event):
    if len(vertex_list[-1]) > 1:
        section = brezenham_int(draw_color, vertex_list[-1][-1].x, vertex_list[-1][-1].y,
                                vertex_list[-1][0].x, vertex_list[-1][0].y)
        draw_section(section)
        vertex_list.append(list())


def brezenham_int(colour, xb, yb, xe, ye):
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


def change_color():
    global draw_color
    draw_color = colorchooser.askcolor(title="select color")[1]
    colour_btn.configure(background=draw_color)


def get_time():
    start_time = time.time()
    solve()
    mb.showinfo("Время.", f"Время построения: {time.time() - start_time: 8.7f}")


def clear_all():
    reset()
    reset_image()


def solve():
    pause = mode.get()
    reset()


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

x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")

point_btn = tk.Button(data_frame, text="Добавить точку", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=put_point,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
solve_btn = tk.Button(data_frame, text="Закрасить", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=solve,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
time_btn = tk.Button(data_frame, text="Измерить время", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=get_time,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
info_btn = tk.Button(data_frame, text="Информация", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
colour_btn = tk.Button(data_frame, text="", font=("Consolas", 14),
                       bg=cfg.DEFAULT_COLOUR, fg=cfg.ADD_COLOUR, command=change_color,
                       relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_all,
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

colour_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                 width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2

x_entry.place(x=0, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
y_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
offset += 1

point_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

offset = cfg.ROWS - 4

solve_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

clear_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
                width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

time_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
               width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1

info_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
               width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)


canvas_frame = tk.Frame(root, bg="white")
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.bind("<Button-1>", left_click)
canvas.bind("<Button-3>", right_click)

img = tk.PhotoImage(width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)
canvas.create_image(
    (cfg.FIELD_WIDTH // 2, cfg.FIELD_HEIGHT // 2), image=img, state='normal')
reset()
reset_image()

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)


print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')


root.mainloop()
