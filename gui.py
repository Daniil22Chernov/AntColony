import tkinter as tk
from PIL import Image, ImageTk
from param import rows, columns, cell_width, cell_height, cells, start_node, end_node, start_point, end_point
from aco import aco

root = tk.Tk()
root.title("Муравьиный алгоритм на графе")
root.state('zoomed')

canvas = tk.Canvas(root, width=600, height=600)
image = Image.open('map4.jpg')
resized_image = image.resize((image.width+20, image.height+45))
photo = ImageTk.PhotoImage(resized_image)
back = canvas.create_image(50, 10, image=photo, anchor="nw")
canvas.pack(fill=tk.BOTH, expand=True)


Start_for_tk = str(start_node)
End_for_tk = str(end_node)


#Buttons


def close():
    root.destroy()

# Функция для рисования сетки и точек
def draw_grid():
    for i in range(rows):
        for j in range(columns):
            x, y = j * cell_width + cell_width, i * cell_height + cell_height // 2
            cell_number = i * columns + j  # Расчет порядкового номера клетки

            if (i, j) == start_point:
                color = "green"
                oval = canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill=color)
            elif (i, j) == end_point:
                color = "blue"
                oval = canvas.create_oval(x - 6, y - 6, x + 6, y + 6, fill=color)
            else:
                oval = canvas.create_oval(x - 6, y - 6, x + 6, y + 6, width=3)
            cells[i][j] = oval

            # Вывод номера клетки под кружком
            canvas.create_text(x, y + 10, text=str(cell_number), fill="black")

draw_grid()
def red(optimal_path):
    # Визуализация пути
    for i in range(len(optimal_path[0]) - 1):
        x1, y1 = (optimal_path[0][i] % columns) * cell_width + cell_width, (optimal_path[0][i] // columns) * cell_height + cell_height // 2
        x2, y2 = (optimal_path[0][i+1] % columns) * cell_width + cell_width, (optimal_path[0][i+1] // columns) * cell_height + cell_height // 2
        canvas.create_line(x1, y1, x2, y2, fill="red", width=2)

    opt_path = 'Оптимальный путь: '
    for i in optimal_path[0]:
        opt_path += str(i) + ' '
    label_text_path = tk.Label(canvas, text=opt_path)
    label_text_path.place(x=750, y=400)

    last_iteration = tk.Label(canvas, text='Окончательная итерация: ' + str(optimal_path[1]))
    last_iteration.place(x=750, y=420)


def Buttons():
    label_text_start = tk.Label(canvas, text='Стартовая точка: ' + Start_for_tk)
    label_text_start.place(x=750, y=360)
    label_text_end = tk.Label(canvas, text='Конечная точка: ' + End_for_tk)
    label_text_end.place(x=750, y=380)
    button = tk.Button(canvas, text='ACO', width=25, height=10, command=lambda: red(aco()))
    button.place(x=750, y=500)  # Размещаем кнопку внутри фрейма
    def on_button_click():
        button.config(bg='gray')
    def on_button_release():
        button.config(bg='white')
    button.bind("<Button-1>", on_button_click())
    button.bind("<ButtonRelease-1>", on_button_release())
    button_end=tk.Button(canvas, text='Закрыть', width=25, height=10, command=close)
    button_end.place(x=1150, y=500)


Buttons()
