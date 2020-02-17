from random import randint
import tkinter as tk
import config as cfg
import tkinter.messagebox as mb

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке
# entry.get()
# label['text'] = ''


def get_limits():
    limits = [[points_list[0], points_list[0]], [points_list[0], points_list[1]]]

    for point in points_list:

        if point[0] < limits[0][0]:
            limits[0][0] = point[0]

        if point[0] > limits[0][1]:
            limits[0][1] = point[0]

        if point[1] < limits[1][0]:
            limits[1][0] = point[1]

        if point[1] > limits[1][1]:
            limits[1][1] = point[1]

        for i in range(2):
            limits[i][0] -= (limits[i][1] - limits[i][0]) * cfg.FIELD_BORDER_PART
            limits[i][1] += (limits[i][1] - limits[i][0]) * cfg.FIELD_BORDER_PART

    return limits


def find_angle(p1, p2, p3):
    # mediana second point (first point for mediana and height is p1).
    pm = [(p2[0] + p3[0]) / 2, (p2[1] + p3[1]) / 2]
    # coefficients for mediana.
    Am = (p1[1] - pm[1])
    Bm = -(p1[0] - pm[0])
    Cm = p1[1] * (p1[0] - pm[0]) - p1[0] * (p1[1] - pm[1])

    # coefficients for height perpendicular (only Bp and Ap 
    # (don't need C, cause we only need angle))
    Ap = (p2[1] - p3[1])
    Bp = -(p2[0] - p3[0])

    # find coefficients for height:
    if Ap == 0:
        Bh = 0
        Ah = 1
        Ch = -p1[0]

    elif Bp == 0:
        Ah = 0
        Bh = 1
        Ch = -p1[1]

    else:
        Bh = 1
        Ah = -(Bp / Ap)
        Ch = -Ah * p1[0] - Bh * p1[1]




def find_solution():
    best_angle = find_angle(points_list[0], points_list[1], points_list[2])
    best_trio = [0, 1, 2]
    limits = get_limits()

    for i in range(len(points_list)):
        for j in range(i + 1, len(points_list)):
            for k in range(j + 1, len(points_list)):
                angle = find_angle(points_list[i], points_list[j], points_list[k])
                if angle < best_angle:
                    best_angle = angle



# points = [p1, p2, p3, height_intersection]
# p1 - vertex where median and height start
def draw_solution(points):
    for i in range(3):
        field.create_line(*points[i], *points[i % 3], width=cfg.LINE_WIDTH, fill="green")
    field.create_line(*points[0], *points[3], width=cfg.LINE_WIDTH, fill="blue")
    field.create_line(*points[0], (points[1][0] + points[2][0]) / 2,
                      (points[1][1] + points[2][1]) / 2, width=cfg.LINE_WIDTH, fill="red")
    # Создание дуги (start - угол начала (в компьютерных координатах (по
    # часовой, 0 - справа)), extent - прирост)
    # c.create_arc(10, 10, 190, 190, start=160, extent=-70, style=ARC, outline='darkblue', width=5)


def translate_to_normal(point: tuple, limits: tuple):
    y = (1 - point[1] / cfg.FIELD_HEIGHT) * \
        (limits[1][1] - limits[1][0]) + limits[1][0]
    x = point[0] / cfg.FIELD_WIDTH * \
        (limits[0][1] - limits[0][0]) + limits[0][0]
    return (x, y)


# limits = ((Xmin, Xmax), (Ymin, Ymax)).
def translate_to_comp(point: tuple, limits: tuple):
    x = (point[0] - limits[0][0]) / (limits[0]
                                     [1] - limits[0][0]) * cfg.FIELD_WIDTH
    y = (1 - (point[1] - limits[1][0]) /
         (limits[1][1] - limits[1][0])) * cfg.FIELD_HEIGHT
    return (x, y)


def add_point(entry1, entry2):
    try:
        x = float(entry1.get())
        y = float(entry2.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
        entry1.delete(0, tk.END)
        entry2.delete(0, tk.END)
    else:
        if (x, y) not in points_list:
            x = f"{x:6g}".strip()
            y = f"{y:6g}".strip()
            points_listbox.insert(tk.END, f"{x}; {y}")
            points_list.append((x, y))

    add_x_entry.delete(0, tk.END)
    add_y_entry.delete(0, tk.END)


def remove_point():
    indeces = list(points_listbox.curselection())
    indeces.reverse()
    for i in indeces:
        points_list.pop(i)
        points_listbox.delete(i)
    return len(indeces)


def sub_point():
    try:
        float(sub_x_entry.get())
        float(sub_y_entry.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
    else:
        number = remove_point()
        if number:
            add_point(sub_x_entry, sub_y_entry)
        else:
            mb.showinfo("Не выбрана точка.",
                        "Если вы хотите просто добавить точку, добавьте через пункт \"Добавить\"")
    sub_x_entry.delete(0, tk.END)
    sub_y_entry.delete(0, tk.END)


points_list = list()
points_list.extend([(randint(1, 1000), randint(1, 1000)) for i in range(100)])


root = tk.Tk()
root.title("Computer graphics 1 lab")
root["bg"] = cfg.MAIN_COLOUR
root.geometry(str(cfg.WINDOW_WIDTH) + "x" + str(cfg.WINDOW_HEIGHT))
root.resizable(height=False, width=False)


input_frame = tk.Frame(root)
input_frame["bg"] = cfg.MAIN_COLOUR

add_button = tk.Button(input_frame, text="Добавить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR,
                       command=lambda: add_point(add_x_entry, add_y_entry),
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

add_x_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")

add_y_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")


sub_button = tk.Button(input_frame, text="Заменить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=sub_point,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

sub_x_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")

sub_y_entry = tk.Entry(input_frame, bg=cfg.ADD_COLOUR, font=("Ubuntu", 15),
                       fg=cfg.MAIN_COLOUR, justify="center")


del_button = tk.Button(input_frame, text="Удалить", font=("Ubuntu", 17),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=remove_point,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

add_x_entry.place(x=0, y=0, width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5)
                  )

add_y_entry.place(x=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2), y=0,
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5)
                  )

add_button.place(x=0, y=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_x_entry.place(x=0, y=int(2 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_y_entry.place(x=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  y=int(2 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH / 2),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

sub_button.place(x=0, y=int(3 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

del_button.place(x=0, y=int(4 * cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5),
                 width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                 height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT / 5))

input_frame.place(x=int(cfg.BORDERS_PART * cfg.WINDOW_WIDTH),
                  y=int(cfg.BORDERS_PART * cfg.WINDOW_HEIGHT),
                  width=int(cfg.INPUT_PART_WIDTH * cfg.WINDOW_WIDTH),
                  height=int(cfg.INPUT_PART_HEIGHT * cfg.WINDOW_HEIGHT)
                  )


data_frame = tk.Frame(root)
data_frame["bg"] = cfg.MAIN_COLOUR

points_listbox = tk.Listbox(data_frame, selectmode=tk.EXTENDED, bg=cfg.ADD_COLOUR,
                            fg=cfg.MAIN_COLOUR, font=("Ubuntu", 14))

scroll = tk.Scrollbar(
    data_frame, command=points_listbox.yview, bg=cfg.MAIN_COLOUR)
points_listbox.config(yscrollcommand=scroll.set)

data_frame.place(x=int(cfg.BORDERS_PART * cfg.WINDOW_WIDTH),
                 y=int((cfg.BORDERS_PART * 2 + cfg.INPUT_PART_HEIGHT)
                       * cfg.WINDOW_HEIGHT),
                 width=int(cfg.WINDOW_WIDTH * cfg.DATA_PART_WIDTH),
                 height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

points_listbox.place(x=0, y=0, width=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
                     height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))

scroll.place(x=int(0.9 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             y=0, width=int(0.1 * cfg.DATA_PART_WIDTH * cfg.WINDOW_WIDTH),
             height=int(cfg.WINDOW_HEIGHT * cfg.DATA_PART_HEIGHT))


field_frame = tk.Frame(root, bg=cfg.ADD_COLOUR)
field = tk.Canvas(field_frame, bg=cfg.ADD_COLOUR)

field_frame.place(x=int((3 * cfg.BORDERS_PART + cfg.INPUT_PART_WIDTH) * cfg.WINDOW_WIDTH),
                  y=int(cfg.BORDERS_PART * cfg.WINDOW_HEIGHT),
                  width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

field.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

for i in range(100):
    points_listbox.insert(tk.END, f"{i}; {i + 1}")

for i in range(2):
    draw_solution(points_list[i * 8:])

root.mainloop()
