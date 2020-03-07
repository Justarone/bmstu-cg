from math import pi, cos, sin, sqrt
import tkinter as tk
import config as cfg
import tkinter.messagebox as mb

# button1.bind("<Button-1>", function) - вызов function при нажатии левой кнопкой мыши на кнопку
# root.bind(chr('a'), function) - действие на кнопке (применяется при наведении на окно root)
# entry.get()
# label['text'] = ''

figure_list = [list(), list(), list()]
back_list = list()
forward_list = list()
A, B, C, D, R = 0, 0, 0, 0, 1


def mul_matrices(matrix1, matrix2):
    result_matrix = [[0 for i in range(3)] for i in range(3)]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                result_matrix[i][j] += matrix1[i][k] * matrix2[k][j]
    return result_matrix


def find_reversed_matrix(matrix):
    det = 0
    for i in range(3):
        det += matrix[0][i] * (matrix[1][(i + 1) % 3] * matrix[2][(i + 2) % 3] -
                               matrix[1][(i + 2) % 3] * matrix[2][(i + 1) % 3])

    new_matrix = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            new_matrix[j][i] = (matrix[(i + 1) % 3][(j + 1) % 3] *
                                  matrix[(i + 2) % 3][(j + 2) % 3] -
                                  matrix[(i + 2) % 3][(j + 1) % 3] *
                                  matrix[(i + 1) % 3][(j + 2) % 3]) / det
    return new_matrix


def show_info():
    mb.showinfo("Информация.", cfg.INFORMATION)


def apply_command(matrix):
    for q in range(len(figure_list)):
        for i in range(len(figure_list[q])):
            new_point = [0, 0, 0]
            for j in range(3):
                for k in range(3):
                    new_point[j] += figure_list[q][i][k] * matrix[j][k]
            figure_list[q][i] = new_point


def enter_params(e_list):
    new_params = list()
    try:
        for e in e_list:
            new_params.append(float(e.get()))
        if new_params[-1] == 0:
            raise ValueError
    except ValueError:
        mb.showerror("Некорректные данные", "Ожидались действительные числа! (При этом R != 0)")
    else:
        global A, B, C, D, R, back_list, forward_list
        A = new_params[0]
        B = new_params[1]
        C = new_params[2]
        D = new_params[3]
        R = new_params[4]
        back_list = list()
        forward_list = list()
        fill_points()
        res_label["text"] = "Новая фигура!\nВсе состояния для\nстарой фигуры сброшены!"


    for e in e_list:
        e.delete(0, tk.END)


def fill_points():
    for i in range(len(figure_list)):
        figure_list[i] = list()
    t = 0
    while (t <= 2 * pi):
        figure_list[0].append([A + cos(t) * R, B + sin(t) * R, 1])
        t += 1 / (R * cfg.SCALE)

    y = -(sqrt(cfg.MAX_LIMIT_X - C) + D)
    while (y < sqrt(cfg.MAX_LIMIT_X - C) + D):
        figure_list[1].append([(y - D) * (y - D) + C, y, 1])
        y += 1 / (cfg.SCALE * 10)

    figure_list[2] = find_zone_points()
    res_label["text"] = f"a = {A:.2f}, b = {B:.2f},\nc = {C:.2f}, d = {D:.2f},\nr = {R:.2f}."
    res_label["text"] += "\nЦентр: (0, 0)."
    draw_figure()

    # Отрисовка примерного отрезка
    p1 = translate_to_comp([cfg.MIN_LIMIT_X + cfg.MAX_LIMIT_X / 6,
                            cfg.MAX_LIMIT_Y / 6 * 4, 1])
    p2 = translate_to_comp([cfg.MIN_LIMIT_X + cfg.MAX_LIMIT_X / 6,
                            cfg.MAX_LIMIT_Y / 6 * 5, 1])
    field.create_line(p1.x, p1.y, p2.x, p2.y, fill="black", arrow=tk.BOTH, width=cfg.LINE_WIDTH)

    p = translate_to_comp([cfg.MIN_LIMIT_X + cfg.MAX_LIMIT_X / 4,
                            cfg.MAX_LIMIT_Y / 6 * 4.5, 1])
    field.create_text(p.x, p.y, text=f"{cfg.MAX_LIMIT_Y / 6:.2f}",
                      justify=tk.CENTER, font="Ubuntu 12")



def change_params():
    top = tk.Toplevel(root)
    top.title("Параметры.")
    top["bg"] = cfg.MAIN_COLOUR
    top.resizable(height=False, width=False)

    labels = list()
    entrys = list()

    for i in "abcdr":
        labels.append(tk.Label(top, bg=cfg.MAIN_COLOUR, font=("Consolas", 15),
                               fg=cfg.ADD_COLOUR, text=i))
        entrys.append(tk.Entry(top, bg=cfg.ADD_COLOUR, font=("Consolas", 15),
                               fg=cfg.MAIN_COLOUR, justify="center"))

    for i in range(5):
        labels[i].grid(row=i, column=0, columnspan=1)
        entrys[i].grid(row=i, column=1, padx=10, columnspan=1)

    ok_btn = tk.Button(top, text="Ok", font=("Consolas", 14),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=lambda: enter_params(entrys),
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
    ok_btn.grid(row=5, column=0)

    top.mainloop()


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x:g}".strip() + "; " + f"{self.y:g}".strip()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def move_figure():
    try:
        x = float(dx_entry.get())
        y = float(dy_entry.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
        res_label["text"] = ""

    else:
        move_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]]
        apply_command(move_matrix)
        back_list.append(find_reversed_matrix(move_matrix))
        res_label["text"] = "Фигура\nперемещена!"

    dx_entry.delete(0, tk.END)
    dy_entry.delete(0, tk.END)
    draw_figure()


def rotate_figure():
    try:
        x = (-1) * float(rx_entry.get())
        y = (-1) * float(ry_entry.get())
        angle = float(angle_entry.get())
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
        res_label["text"] = ""

    else:
        move_matrix = [[1, 0, -x], [0, 1, -y], [0, 0, 1]]
        rotate_matrix = [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]
        unmove_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]]

        result_matrix = mul_matrices(move_matrix, rotate_matrix)
        result_matrix = mul_matrices(result_matrix, unmove_matrix)

        apply_command(result_matrix)
        back_list.append(find_reversed_matrix(result_matrix))
        res_label["text"] = "Фигура\nповернута!"

    rx_entry.delete(0, tk.END)
    ry_entry.delete(0, tk.END)
    angle_entry.delete(0, tk.END)
    draw_figure()


def scale_figure():
    try:
        x = (-1) * float(scx_entry.get())
        y = (-1) * float(scy_entry.get())
        kx = float(sx_entry.get())
        ky = float(sy_entry.get())
        if not kx or not ky:
            raise ZeroDivisionError
    except ValueError:
        mb.showerror("Неверный ввод",
                     "Введите действительные числа в поля ввода")
        res_label["text"] = ""
    except ZeroDivisionError:
        mb.showerror("Плохие данные.", "При данных значениях масштабирования фигура " \
                     "превратится либо в точку, либо в прямую. Не допускаю!")
        res_label["text"] = ""

    else:
        move_matrix = [[1, 0, -x], [0, 1, -y], [0, 0, 1]]
        scale_matrix = [[kx, 0, 0], [0, ky, 0], [0, 0, 1]]
        unmove_matrix = [[1, 0, x], [0, 1, y], [0, 0, 1]]

        result_matrix = mul_matrices(move_matrix, scale_matrix)
        result_matrix = mul_matrices(result_matrix, unmove_matrix)

        apply_command(result_matrix)
        back_list.append(find_reversed_matrix(result_matrix))
        res_label["text"] = "Фигура\nотмасштабирована!"

    scx_entry.delete(0, tk.END)
    scy_entry.delete(0, tk.END)
    sx_entry.delete(0, tk.END)
    sy_entry.delete(0, tk.END)
    draw_figure()


def back_figure():
    if back_list:
        matrix = back_list.pop()
        apply_command(matrix)
        forward_list.append(find_reversed_matrix(matrix))
        draw_figure()
        res_label["text"] = "Предыдущее\nсостояние."
    else:
        res_label["text"] = "Вы в самом\nстаром состоянии."


def forward_figure():
    if forward_list:
        matrix = forward_list.pop()
        apply_command(matrix)
        back_list.append(find_reversed_matrix(matrix))
        draw_figure()
        res_label["text"] = "Следующее\nсостояние."
    else:
        res_label["text"] = "Вы в самом\nновом состоянии."


def translate_to_comp(point_vector):
    x = int((point_vector[0] - cfg.MIN_LIMIT_X) /
            (cfg.MAX_LIMIT_X - cfg.MIN_LIMIT_X) * cfg.FIELD_WIDTH)
    y = int((1 - (point_vector[1] - cfg.MIN_LIMIT_Y) /
             (cfg.MAX_LIMIT_Y - cfg.MIN_LIMIT_Y)) * cfg.FIELD_HEIGHT)
    return Point(x, y)


def find_zone_points():
    zone_points = list()
    for plist in figure_list:
        zone_points.extend(
            list(filter(lambda x: (x[0] - A) ** 2 + (x[1] - B) ** 2 <= R * R \
                        and x[0] >= C + (x[1] - D) ** 2, plist)))
    return zone_points


def draw_lines():
    step = cfg.STEP
    zone_points = figure_list[2]
    min_b, max_b = None, None

    for pts in zone_points:
        b = pts[1] - cfg.INCLINE * pts[0]

        if not min_b or b < min_b:
            min_pts = pts
            min_b = b

        if not max_b or b > max_b:
            max_b = b
            max_pts = pts

    c = (max_pts[1] - min_pts[1]) / (max_pts[0] - min_pts[0])

    half_b = max_pts[1] - c * max_pts[0]
    # p1 = translate_to_comp([-1000, c * -1000 + half_b, 1])
    # p2 = translate_to_comp([1000, c * 1000 + half_b, 1])
    # field.create_line(p1.x, p1.y, p2.x, p2.y, fill="blue")

    z1, z2 = list(), list()
    for pts in zone_points:
        if pts[1] - c * pts[0] < half_b:
            z1.append(pts)
        else:
            z2.append(pts)

    z1.sort(key=lambda x: x[1] - cfg.INCLINE * x[0])
    z2.sort(key=lambda x: x[1] - cfg.INCLINE * x[0])

    cur_b = min_b

    while cur_b < max_b:
        draw_line(cur_b, z1, z2, cfg.INCLINE)
        cur_b += step


def draw_line(b, z1, z2, incline):
    global field
    points = list()

    i = 0
    while i < len(z1) - 1 and z1[i][1] - incline * z1[i][0] < b:
        i += 1
    points.append(translate_to_comp(z1[i]))

    i = 0
    while i < len(z2) - 1 and z2[i][1] - incline * z2[i][0] < b:
        i += 1
    points.append(translate_to_comp(z2[i]))

    field.create_line(points[0].x, points[0].y, points[1].x, points[1].y, width=cfg.LINE_WIDTH,
                      fill="red")


def draw_figure():
    global field
    field.delete("all")

    # draw center
    center = translate_to_comp([0, 0, 1])

    # draw axises
    p1 = translate_to_comp([cfg.MIN_LIMIT_X, 0, 1])
    p2 = translate_to_comp([cfg.MAX_LIMIT_X, 0, 1])
    field.create_line(p1.x, p1.y, p2.x, p2.y, fill="black", arrow=tk.LAST, width=cfg.LINE_WIDTH)
    p1 = translate_to_comp([0, cfg.MIN_LIMIT_Y, 1])
    p2 = translate_to_comp([0, cfg.MAX_LIMIT_Y, 1])
    field.create_line(p1.x, p1.y, p2.x, p2.y, fill="black", arrow=tk.LAST, width=cfg.LINE_WIDTH)

    field.create_oval(center.x, center.y, center.x, center.y,
                      width = cfg.POINT_SIZE, fill = "black")
    for k in range(len(figure_list) - 1):
        p1 = translate_to_comp(figure_list[k][0])

        # "Дорисовка" окружности
        if k == 0:
            p2 = translate_to_comp(figure_list[k][-1])
            field.create_line(p1.x, p1.y, p2.x, p2.y, fill="green", width=cfg.LINE_WIDTH)

        for i in range(1, len(figure_list[k])):
            p2 = translate_to_comp(figure_list[k][i])
            field.create_line(p1.x, p1.y, p2.x, p2.y, fill="green", width=cfg.LINE_WIDTH)
            p1 = p2
    draw_lines()


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

# For move command.
dx_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 15),
                   fg=cfg.MAIN_COLOUR, justify="center")
dy_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 15),
                   fg=cfg.MAIN_COLOUR, justify="center")

# For rotate_command.
rx_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
ry_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                   fg=cfg.MAIN_COLOUR, justify="center")
angle_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 13),
                       fg=cfg.MAIN_COLOUR, justify="center")

# For scale command.
sx_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 10),
                   fg=cfg.MAIN_COLOUR, justify="center")
sy_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 10),
                   fg=cfg.MAIN_COLOUR, justify="center")
scx_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 10),
                       fg=cfg.MAIN_COLOUR, justify="center")
scy_entry = tk.Entry(data_frame, bg=cfg.ADD_COLOUR, font=("Consolas", 10),
                       fg=cfg.MAIN_COLOUR, justify="center")


move_btn = tk.Button(data_frame, text="Переместить", font=("Consolas", 14),
                     bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=move_figure,
                     activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
rotate_btn = tk.Button(data_frame, text="Повернуть", font=("Consolas", 14),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=rotate_figure,
                       activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)
scale_btn = tk.Button(data_frame, text="Масштабировать", font=("Consolas", 14),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=scale_figure,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

back_btn = tk.Button(data_frame, text="<--", font=("Consolas", 24),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=back_figure,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

forward_btn = tk.Button(data_frame, text="-->", font=("Consolas", 24),
                      bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=forward_figure,
                      activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)


move_label = tk.Label(data_frame, text="ПЕРЕМЕЩЕНИЕ.\n(Ввод dx, dy," \
                      "\nгде dx, dy - перемещение\nпо х и по у соответственно)",
                      font=("Consolas", 9), bg=cfg.MAIN_COLOUR,
                      fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

rotate_label = tk.Label(data_frame, text="ПОВОРОТ.\n(Ввод x, y, angle," \
                        "\nгде x, y - координаты \nцентра поворота,"\
                      " angle - \nугол поворота в радианах)", font=("Consolas", 9),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

scale_label = tk.Label(data_frame, text="МАСШТАБИРОВАНИЕ.\n(Ввод kx, ky, Mx, My," \
                       "\nгде М - центр масштабирования,\n" \
                      "kx, ky - коэффициенты \nмасштабирования)", font=("Consolas", 9),
                       bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, relief=tk.GROOVE)

move_label.place(x=0, y=0, width=cfg.DATA_WIDTH, height=2 * cfg.DATA_HEIGHT // cfg.COLUMNS)
dx_entry.place(x=0, y=2 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH // 2,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
dy_entry.place(x=cfg.DATA_WIDTH // 2, y=2 * cfg.DATA_HEIGHT // cfg.COLUMNS,
               width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
move_btn.place(x=0, y=3 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)

rotate_label.place(x=0, y=4 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
                   height=2 * cfg.DATA_HEIGHT // cfg.COLUMNS)
rx_entry.place(x=0, y=6 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH // 3,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
ry_entry.place(x=cfg.DATA_WIDTH // 3, y=6 * cfg.DATA_HEIGHT // cfg.COLUMNS,
              width=cfg.DATA_WIDTH // 3, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
angle_entry.place(x=2 * cfg.DATA_WIDTH // 3, y=6 * cfg.DATA_HEIGHT // cfg.COLUMNS,
                 width=cfg.DATA_WIDTH // 3, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
rotate_btn.place(x=0, y=7 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
                 height=cfg.DATA_HEIGHT // cfg.COLUMNS)

scale_label.place(x=0, y=8 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
                  height=2 * cfg.DATA_HEIGHT // cfg.COLUMNS)
sx_entry.place(x=0, y=10 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH // 4,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
sy_entry.place(x=cfg.DATA_WIDTH // 4, y=10 * cfg.DATA_HEIGHT // cfg.COLUMNS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
scx_entry.place(x=2 * cfg.DATA_WIDTH // 4, y=10 * cfg.DATA_HEIGHT // cfg.COLUMNS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
scy_entry.place(x=3 * cfg.DATA_WIDTH // 4, y=10 * cfg.DATA_HEIGHT // cfg.COLUMNS,
               width=cfg.DATA_WIDTH // 4, height=cfg.DATA_HEIGHT // cfg.COLUMNS)
scale_btn.place(x=0, y=11 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH,
                height=cfg.DATA_HEIGHT // cfg.COLUMNS)
back_btn.place(x=0, y=12 * cfg.DATA_HEIGHT // cfg.COLUMNS, width=cfg.DATA_WIDTH // 2,
               height=cfg.DATA_HEIGHT // cfg.COLUMNS)
forward_btn.place(x=cfg.DATA_WIDTH // 2, y=12 * cfg.DATA_HEIGHT // cfg.COLUMNS,
                  width=cfg.DATA_WIDTH // 2, height=cfg.DATA_HEIGHT // cfg.COLUMNS)


field_frame = tk.Frame(root, bg=cfg.ADD_COLOUR)
field = tk.Canvas(field_frame, bg=cfg.ADD_COLOUR)

field_frame.place(x=3 * cfg.BORDERS_WIDTH + cfg.DATA_WIDTH, y=cfg.BORDERS_HEIGHT, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)

field.place(x=0, y=0, width=cfg.FIELD_WIDTH, height=cfg.FIELD_HEIGHT)


info_frame = tk.Frame(root)
info_frame["bg"] = cfg.ADD_COLOUR

info_frame.place(x=cfg.BORDERS_WIDTH, y=cfg.DATA_HEIGHT + 2 * cfg.BORDERS_HEIGHT,
                 width=cfg.INFO_WIDTH, height=cfg.INFO_HEIGHT)

info_button = tk.Button(info_frame, text="i", font=("Consolas", 20),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=show_info,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

params_btn = tk.Button(info_frame, text="Параметры", font=("Consolas", 15),
                        bg=cfg.MAIN_COLOUR, fg=cfg.ADD_COLOUR, command=change_params,
                        activebackground=cfg.ADD_COLOUR, activeforeground=cfg.MAIN_COLOUR)

res_label = tk.Label(info_frame, text="", font=("Consolas", 12), fg=cfg.MAIN_COLOUR, bg=cfg.ADD_COLOUR)

res_label.place(x=0, y=0, width=cfg.INFO_WIDTH,
                height=cfg.INFO_HEIGHT * (cfg.INFO_COLS - 1) // cfg.INFO_COLS)
params_btn.place(x=0, y=cfg.INFO_HEIGHT * (cfg.INFO_COLS - 1) // cfg.INFO_COLS,
                  width=4 / 5 * cfg.INFO_WIDTH, height=cfg.INFO_HEIGHT // cfg.INFO_COLS)
info_button.place(x=4 / 5 * cfg.INFO_WIDTH,
                  y=cfg.INFO_HEIGHT * (cfg.INFO_COLS - 1) // cfg.INFO_COLS,
                  width=1 / 5 * cfg.INFO_WIDTH, height=cfg.INFO_HEIGHT // cfg.INFO_COLS)

fill_points()


root.mainloop()
