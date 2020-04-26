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
    solve()

def right_click(event):
    if not left_corner[0]:
        left_corner[0], left_corner[1] = event.x, event.y
    else:
        new_rect(left_corner[0], left_corner[1], event.x, event.y)


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
    pass


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

rect_left_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_right_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_up_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
rect_down_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")

rect_btn = tk.Button(data_frame, text="Применить", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=read_rect,
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
offset += 3

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
