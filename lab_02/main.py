from math import pi, atan
import tkinter as tk
import config as cfg
import tkinter.messagebox as mb

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке (применяется при наведении на окно root)
# entry.get()
# label['text'] = ''


def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x:g}".strip() + "; " + f"{self.y:g}".strip()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def find_solution():
    pass


def draw_solution(points, best_angle):
    pass


def translate_to_comp(point: Point):
    x = int((point.x - cfg.MIN_LIMIT_X) /
            (cfg.MAX_LIMIT_X - cfg.MIN_LIMIT_X) * cfg.FIELD_WIDTH)
    y = int((1 - (point.y - cfg.MIN_LIMIT_Y) /
             (cfg.MAX_LIMIT_Y - cfg.MIN_LIMIT_Y)) * cfg.FIELD_HEIGHT)
    return Point(x, y)


root = tk.Tk()
root.title("Computer graphics 2 lab.")
root["bg"] = cfg.MAIN_COLOUR
root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)
# root.bind("<Return>", lambda x: find_solution())


data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

data_frame.place(x=int(cfg.BORDERS_WIDTH), y=int(cfg.BORDERS_HEIGHT),
                 width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT
                 )

x_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                   fg=cfg.MAIN_COLOUR, justify="center")
y_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                   fg=cfg.MAIN_COLOUR, justify="center")
value_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")

info_label = tk.Label(label_frame, text="x  |  y  | value", font=("Ubuntu", 11),
                       fg=cfg.MAIN_COLOUR, bg=cfg.ADD_COLOUR)

move_btn = tk.Button(data_frame, text="Move", font=("Ubuntu", 17),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=move_figure,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
rotate_btn = tk.Button(data_frame, text="Move", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_figure,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
scale_btn = tk.Button(data_frame, text="Move", font=("Ubuntu", 17),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=scale_figure,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)


info_button = tk.Button(root, text="i", font=("Ubuntu", 27),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

root.mainloop()
