import time
import numpy as np
import tkinter as tk
from tkinter import colorchooser
import config as cfg
import tkinter.messagebox as mb


cutter_color = cfg.DEFAULT_COLOUR
sect_color = cfg.DEFAULT_COLOUR
res_color = cfg.DEFAULT_COLOUR
verteces_list = []
sections = []
figure_list = []


def clear_all():
    clear_canvas() 
    sections.clear()
    verteces_list.clear()


def clear_canvas():
    canvas.delete('all')


def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


def left_click(event):
    figure_list.append([event.x, event.y])
    if len(figure_list) >= 2:
        draw_section(*figure_list[-1], *figure_list[-2], sect_color)
    

def return_click(event):
    if len(verteces_list) < 3:
        return
    draw_section(*verteces_list[-1], *verteces_list[0], cutter_color)


def c_click(event):
    if len(figure_list) < 3:
        return
    draw_section(*figure_list[-1], *figure_list[0], sect_color)


def right_click(event):
    verteces_list.append([event.x, event.y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)


def read_cutter_vertex():
    try:
        x = int(cutter_x_entry.get())
        y = int(cutter_y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины (учтите, что при работе с растром \
                      коориданаты должны быть целыми)")
    verteces_list.append([x, y])
    if len(verteces_list) >= 2:
        draw_section(*verteces_list[-1], *verteces_list[-2], cutter_color)


def draw_section(xb, yb, xe, ye, color):
    canvas.create_line(xb, yb, xe, ye, fill=color)


def read_vertex():
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины (учтите, что при работе с растром \
                      коориданаты должны быть целыми)")
    figure_list.append([x, y])
    if len(figure_list) >= 2:
        draw_section(*figure_list[-1], *figure_list[-2], cutter_color)


def change_cutter_color():
    global cutter_color
    cutter_color = colorchooser.askcolor(title="select color")[1]
    cutter_color_btn.configure(background=cutter_color)


def change_sect_color():
    global sect_color
    sect_color = colorchooser.askcolor(title="select color")[1]
    sect_color_btn.configure(background=sect_color)


def change_res_color():
    global res_color
    res_color = colorchooser.askcolor(title="select color")[1]
    res_color_btn.configure(background=res_color)


def get_vect(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]


def vect_mul(v1, v2):
    return v1[0] * v2[1] - v1[1] * v2[0]

def scalar_mul(v1, v2):
    return v1[0] * v2[0] + v1[1] * v2[1]


def check_polygon(verteces):
    if len(verteces) < 3:
        return False
    sign = 1 if vect_mul(get_vect(verteces[1], verteces[2]),
                         get_vect(verteces[0], verteces[1])) > 0 else -1
    for i in range(3, len(verteces)):
        if sign * vect_mul(get_vect(verteces[i - 1], verteces[i]),
                           get_vect(verteces[i - 2], verteces[i - 1])) < 0:
            return False

    if sign < 0:
        verteces.reverse()

    # CHECK: for verteces order
    # for i, c in enumerate(verteces):
        # canvas.create_oval(c[0] - i * 3, c[1] - i * 3, c[0] + i * 3, c[1] + i * 3, fill="green")

    return True


# cp = check point
def get_normal(p1, p2, cp):
    vect = get_vect(p1, p2)
    norm = [1, 0] if vect[0] == 0 else [-vect[1] / vect[0], 1]
    if scalar_mul(get_vect(p2, cp), norm) < 0:
        for i in range(len(norm)):
            norm[i] = -norm[i]

    # CHECK: for normal direction and side
    # center = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
    # draw_section(center[0], center[1], center[0] + 10 * norm[0], center[1] + 10 * norm[1], cutter_color)

    return norm


def get_normals_list(verteces):
    length = len(verteces)
    normal_list = list()
    for i in range(length):
        normal_list.append(get_normal(verteces[i], verteces[(i + 1) % length], verteces[(i + 2) % length]))

    return normal_list


def cut_figure():
    pass


def solve():
    if not check_polygon(verteces_list):
        mb.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека \
                     прямоугольник должен быть выпуклым")
        return
    # CHEAT PART ================================================
    big_list = list()
    for vertex in verteces_list:
        big_list.extend(vertex)
    canvas.create_polygon(*big_list, outline=cutter_color, fill=cfg.CANVAS_COLOUR)
    # CHEAT PART ENDS ===========================================
    normals_list = get_normals_list(verteces_list)
    cut_figure()


root = tk.Tk()
root.title("Computer graphics 8 lab.")
root["bg"] = cfg.MAIN_COLOUR

data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

cutter_color_label = tk.Label(data_frame, text="Цвет регулярного отсекателя", font=("Consolas", 14),
                            bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
sect_color_label = tk.Label(data_frame, text="Цвет отрезков", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                            fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
res_color_label = tk.Label(data_frame, text="Цвет результата", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                           fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
cutter_label = tk.Label(data_frame, text="Ввод вершины отсекателя", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
vertex_label = tk.Label(data_frame, text="Ввод вершины многоугольника", font=("Consolas", 14),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
x_label = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
y_label = tk.Label(data_frame, text="y", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
cutter_x_label = tk.Label(data_frame, text="x", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
cutter_y_label = tk.Label(data_frame, text="y", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)


cutter_x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
cutter_y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")


cutter_btn = tk.Button(data_frame, text="Добавить вершину", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=read_cutter_vertex,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
close_cutter_btn = tk.Button(data_frame, text="Замкнуть отсекатель", font=("Consolas", 14),
                             bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=lambda: return_click(0),
                             activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
close_btn = tk.Button(data_frame, text="Замкнуть многоугольник", font=("Consolas", 14),
                             bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=lambda: c_click(0),
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

cutter_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14), bg=cutter_color,
                             command=change_cutter_color, relief=tk.GROOVE)
sect_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14), bg=sect_color,
                           command=change_sect_color, relief=tk.GROOVE)
res_color_btn = tk.Button(data_frame, text="", font=("Consolas", 14), bg=res_color,
                          command=change_res_color, relief=tk.GROOVE)
clear_btn = tk.Button(data_frame, text="Очистить поле", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=clear_all,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

offset = 0

cutter_color_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
cutter_color_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset,
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

cutter_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
cutter_x_label.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
cutter_y_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
cutter_x_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
cutter_y_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)

offset += 1
cutter_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2
close_cutter_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 3

vertex_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1
x_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
y_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
offset += 1
x_entry.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
y_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
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
root.bind("c", c_click)
canvas.bind("<Button-3>", right_click)

canvas_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT,
                   width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

canvas.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

print("Canvas params: ", cfg.FIELD_WIDTH, "x", cfg.FIELD_HEIGHT, sep='')

root.mainloop()
