import random

rows =12
columns = 12

cell_width, cell_height = 56, 56
cells = [[None] * columns for _ in range(rows)]

mount_point = [6, 7, 17, 18, 19, 28, 29, 40, 41, 42, 43, 53, 54, 65, 66, 77, 90]

start_node = random.randint(0, rows*columns-1)
while start_node in mount_point:
    start_node = random.randint(0, rows*columns-1)
end_node = random.randint(0, rows*columns-1)
while start_node == end_node or end_node in mount_point:
       end_node = random.randint(0, rows*columns-1)

#start_node = 0
#end_node = 5
start_point = (start_node // columns, start_node % columns)
end_point = (end_node // columns, end_node % columns)

adj_matrix = [[0 for _ in range(rows * columns)] for _ in range(rows * columns)]
opt_path = 'Оптимальный путь: '
# Заполняем матрицу смежности на основе графа
for i in range(rows):
    for j in range(columns):
        if i > 0:  # Можем двигаться вверх
            adj_matrix[i * columns + j][(i - 1) * columns + j] = 1
        if i < rows - 1:  # Можем двигаться вниз
            adj_matrix[i * columns + j][(i + 1) * columns + j] = 1
        if j > 0:  # Можем двигаться влево
            adj_matrix[i * columns + j][i * columns + (j - 1)] = 1
        if j < columns - 1:  # Можем двигаться вправо
            adj_matrix[i * columns + j][i * columns + (j + 1)] = 1

num_ants = 10
alpha = 5.0
beta = 2.0
evaporation_rate = 0.5
pheromone_constant = 1.0
iterations = 40