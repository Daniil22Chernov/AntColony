from param import rows, columns, end_node, adj_matrix, num_ants, evaporation_rate, iterations, start_node, alpha, beta, mount_point
import random


# Определение веса позитивного феромона
def Pos_pheromone_weight(current, destination, end):
    end_x, end_y = end // columns, end % columns
    current_x, current_y = current // columns, current % columns
    destination_x, destination_y = destination // columns, destination % columns

    # Определяем направление к цели от текущей позиции
    direction_to_end = (end_x - current_x, end_y - current_y)
    # Определяем направление движения от текущей позиции к следующей
    move_direction = (destination_x - current_x, destination_y - current_y)

    # Нормализация направления к цели
    norm_direction_to_end = (0 if direction_to_end[0] == 0 else direction_to_end[0]//abs(direction_to_end[0]),
                             0 if direction_to_end[1] == 0 else direction_to_end[1]//abs(direction_to_end[1]))

    # Нормализация направления движения
    norm_move_direction = (0 if move_direction[0] == 0 else move_direction[0]//abs(move_direction[0]),
                           0 if move_direction[1] == 0 else move_direction[1]//abs(move_direction[1]))


    # Сравниваем нормализованные направления
    if destination in mount_point:
        return 1
    elif norm_move_direction == norm_direction_to_end:
        return 0.5  # Движение напрямую к цели
    elif norm_move_direction[0] == norm_direction_to_end[0] or norm_move_direction[1] == norm_direction_to_end[1]:
        if norm_move_direction[0] != 0 and norm_move_direction[1] != 0:
            return 0.37  # Движение по диагонали к цели
        else:
            return 0.15  # Движение горизонтально или вертикально, но не напрямую к цели
    elif norm_move_direction == tuple(map(lambda x: x * -1, norm_direction_to_end)):
        return 0.05  # Движение напрямую от цели
    elif (norm_move_direction[0] != 0 and norm_move_direction[1] != 0) and \
         (norm_move_direction[0] != norm_direction_to_end[0] or norm_move_direction[1] != norm_direction_to_end[1]):
        return 0.1  # Движение по диагонали от цели
    else:
        return 0.01  # Непредвиденное направление движения или ошибка


# Определение веса негативного феромона
def Neg_pheromone_weight(current, destination, end):
    end_x, end_y = end // columns, end % columns
    current_x, current_y = current // columns, current % columns
    destination_x, destination_y = destination // columns, destination % columns

    # Определяем направление к цели от текущей позиции
    direction_to_end = (end_x - current_x, end_y - current_y)
    # Определяем направление движения от текущей позиции к следующей
    move_direction = (destination_x - current_x, destination_y - current_y)

    # Нормализация направления к цели
    norm_direction_to_end = (0 if direction_to_end[0] == 0 else direction_to_end[0]//abs(direction_to_end[0]),
                             0 if direction_to_end[1] == 0 else direction_to_end[1]//abs(direction_to_end[1]))

    # Нормализация направления движения
    norm_move_direction = (0 if move_direction[0] == 0 else move_direction[0]//abs(move_direction[0]),
                           0 if move_direction[1] == 0 else move_direction[1]//abs(move_direction[1]))

    # Сравниваем нормализованные направления
    if destination in mount_point:
        return 0.99
    elif norm_move_direction == norm_direction_to_end:
        return 0.2  # Движение напрямую к цели
    elif norm_move_direction[0] == norm_direction_to_end[0] or norm_move_direction[1] == norm_direction_to_end[1]:
        if norm_move_direction[0] != 0 and norm_move_direction[1] != 0:
            return 0.1  # Движение по диагонали к цели
        else:
            return 0.05  # Движение горизонтально или вертикально, но не напрямую к цели
    elif norm_move_direction == tuple(map(lambda x: x * -1, norm_direction_to_end)):
        return 0.4  # Движение напрямую от цели
    elif (norm_move_direction[0] != 0 and norm_move_direction[1] != 0) and \
         (norm_move_direction[0] != norm_direction_to_end[0] or norm_move_direction[1] != norm_direction_to_end[1]):
        return 0.03  # Движение по диагонали от цели
    else:
        return 0.001  # Непредвиденное направление движения или ошибка


# Инициализируем феромоны с учетом расстояний
def initialize_pheromones(rows, columns, end_node):
    pheromones = [[0 for _ in range(rows * columns)] for _ in range(rows * columns)]
    for i in range(rows * columns):
        for j in range(rows * columns):
            pheromones[i][j] = 1
            #if adj_matrix[i][j] == 1:
                #pheromones[i][j] = Pos_pheromone_weight(i, j, end_node) - Neg_pheromone_weight(i, j, end_node)
    return pheromones


# Создаем список для хранения феромонов на ребрах с начальными значениями
pheromone = initialize_pheromones(rows, columns, end_node)


def aco():
    all_paths = []
    last_it = 0
    # Главный цикл алгоритма муравьиных колоний
    for it in range(iterations):
        for i in range(rows * columns):
            for j in range(rows * columns):
                pheromone[i][j] *= (1 - evaporation_rate)

        # На каждой итерации создаем новый список для хранения пути каждого муравья
        current_iteration_paths = []

        for ant in range(num_ants):
            current_node = start_node
            path = [current_node]
            visited = set(path)

            while current_node != end_node:
                available_nodes = [node for node in range(rows * columns) if adj_matrix[current_node][node] == 1 and node not in visited and node not in mount_point]
                if available_nodes:
                    tau_shift = [pheromone[current_node][node] + min(pheromone[current_node]) for node in range(rows*columns)]  # Сдвиг феромона
                    probabilities = [((tau_shift[node] ** alpha) * ((1.0 / adj_matrix[current_node][node]) ** beta)) for node in available_nodes]
                    probabilities = [prob / sum(probabilities) for prob in probabilities]
                    next_node = random.choices(available_nodes, weights=probabilities, k=1)[0]
                    path.append(next_node)
                    visited.add(next_node)
                    current_node = next_node
                else:  # муравей зашел в тупик, необходимо откатиться
                    path.pop()  # Удаляем последний узел из пути
                    if path:  # Если путь не пустой, возвращаемся к предыдущему узлу
                        current_node = path[-1]
                    else:  # Если путь пустой, муравей не может найти путь, начинаем сначала
                        break

            # Добавляем текущий путь в список всех найденных путей для текущей итерации
            current_iteration_paths.append(path[:])

        # Обновляем феромоны на пройденном пути
        for i in range(len(current_iteration_paths) - 1):
            for j in range(len(current_iteration_paths[i]) - 1):
                pheromone_weight_value = Pos_pheromone_weight(current_iteration_paths[i][j], current_iteration_paths[i][j+1], end_node) - Neg_pheromone_weight(current_iteration_paths[i][j], current_iteration_paths[i][j+1], end_node)
                pheromone[current_iteration_paths[i][j]][current_iteration_paths[i][j+1]] += pheromone_weight_value
                pheromone[current_iteration_paths[i][j+1]][current_iteration_paths[i][j]] += pheromone_weight_value

        if len(all_paths) > 1:
            if all_paths[-2] == all_paths[-1]:
                last_it = it
                break

        # Добавляем все пути текущей итерации в список всех путей
        all_paths.extend(current_iteration_paths)

    # Найденный оптимальный путь
    optimal_path = min(all_paths, key=lambda x: len(x))
    return optimal_path, last_it