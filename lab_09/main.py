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
    figure_list.clear()


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


def read_vertex():
    try:
        x = int(x_entry.get())
        y = int(y_entry.get())
    except:
        mb.showerror("Неверный ввод", "Не удалось считать коориданаты очередной вершины (учтите, что при работе с растром \
                      коориданаты должны быть целыми)")
    figure_list.append([x, y])
    if len(figure_list) >= 2:
        draw_section(*figure_list[-1], *figure_list[-2], sect_color)


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


def draw_section(xb, yb, xe, ye, color):
        #======================================== CHEAT ===================================
        canvas.create_line(xb, yb, xe, ye, fill=cfg.CANVAS_COLOUR, width=2)
        # =================================================================================
        canvas.create_line(xb, yb, xe, ye, fill=color)


def make_uniq(sections):
    for section in sections:
        section.sort()
    return list(filter(lambda x: (sections.count(x) % 2) == 1, sections))


def point_in_section(point, section):
    if abs(vect_mul(get_vect(point, section[0]), get_vect(*section))) <= 1e-6:
        if (section[0] < point < section[1] or section[1] < point < section[0]):
            return True
    return False


def get_sections(section, rest_points):
    points_list = [section[0], section[1]]
    for p in rest_points:
        if point_in_section(p, section):
            points_list.append(p)

    points_list.sort()

    sections_list = list()
    for i in range(len(points_list) - 1):
        sections_list.append([points_list[i], points_list[i + 1]])

    return sections_list



def get_uniq_sections(figure):
    all_sections = list()
    rest_points = figure[2:]
    for i in range(len(figure)):
        cur_section = [figure[i], figure[(i + 1) % len(figure)]]

        all_sections.extend(get_sections(cur_section, rest_points))

        rest_points.pop(0)
        rest_points.append(figure[i])

    return make_uniq(all_sections)


def draw_figure(figure):
    for section in get_uniq_sections(figure):
        draw_section(round(section[0][0]), round(section[0][1]), round(section[1][0]), round(section[1][1]), res_color)


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
    length = len(verteces_list)
    normal_list = list()
    for i in range(length):
        normal_list.append(get_normal(verteces[i], verteces[(i + 1) % length], verteces[(i + 2) % length]))

    return normal_list


def check_point(point, p1, p2):
    return True if vect_mul(get_vect(p1, p2), get_vect(p1, point)) <= 0 else False


def find_intersection(section, edge, normal):
    wi = get_vect(edge[0], section[0])
    d = get_vect(section[0], section[1])
    Wck = scalar_mul(wi, normal)
    Dck = scalar_mul(d, normal)

    diff = [section[1][0] - section[0][0], section[1][1] - section[0][1]]
    t = -Wck / Dck

    return [section[0][0] + diff[0] * t, section[0][1] + diff[1] * t]



def edgecut_figure(figure, edge, normal):
    res_figure = list()
    if len(figure) < 3:
        return []

    prev_check = check_point(figure[0], *edge)

    for i in range(1, len(figure) + 1):
        cur_check = check_point(figure[i % len(figure)], *edge)

        if prev_check:
            if cur_check:
                res_figure.append(figure[i % len(figure)])
            else:
                res_figure.append(find_intersection([figure[i - 1], figure[i % len(figure)]], edge, normal))

        else:
            if cur_check:
                res_figure.append(find_intersection([figure[i - 1], figure[i % len(figure)]], edge, normal))
                res_figure.append(figure[i % len(figure)])

        prev_check = cur_check

    return res_figure


def cut_figure(figure, cutter_verteces, normals_list):
    res_figure = figure
    for i in range(len(cutter_verteces)):
        cur_edge = [cutter_verteces[i], cutter_verteces[(i + 1) % len(cutter_verteces)]]
        res_figure = edgecut_figure(res_figure, cur_edge, normals_list[i])
        if len(res_figure) < 3:
            return []

    return res_figure


def solve():
    if not check_polygon(verteces_list):
        mb.showerror("Невыпуклый многоугольник", "Для осуществления отсечения отрезка алгоритмом Кируса-Бека \
                     прямоугольник должен быть выпуклым")
        return
    normals_list = get_normals_list(verteces_list)
    cutted_figure = cut_figure(figure_list, verteces_list, normals_list)
    draw_figure(cutted_figure)


root = tk.Tk()
root.title("Computer graphics 9 lab.")
root["bg"] = cfg.MAIN_COLOUR

data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

cutter_color_label = tk.Label(data_frame, text="Цвет отсекателя", font=("Consolas", 14),
                            bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)
sect_color_label = tk.Label(data_frame, text="Цвет многоугольника", font=("Consolas", 14), bg=cfg.MAIN_COLOUR,
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
cutter_y_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                     width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.ROWS)
offset += 1
cutter_x_entry.place(x=0, y=cfg.DATA_HEIGHT * offset // cfg.ROWS, width=cfg.DATA_WIDTH // 2,
                       height=cfg.DATA_HEIGHT // cfg.ROWS)
cutter_y_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.DATA_HEIGHT * offset // cfg.ROWS,
                     width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.ROWS)

offset += 1
cutter_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 2
close_cutter_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 3

vertex_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)
offset += 1
x_label.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
y_label.place(x=cfg.DATA_WIDTH // 2, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
offset += 1
x_entry.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
y_entry.place(x=cfg.DATA_WIDTH // 2, y=cfg.SLOT_HEIGHT * offset,
              width=cfg.DATA_WIDTH // 2, height=cfg.SLOT_HEIGHT)
offset += 1
vertex_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

offset += 2
close_btn.place(x=0, y=cfg.SLOT_HEIGHT * offset, width=cfg.DATA_WIDTH, height=cfg.SLOT_HEIGHT)

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
