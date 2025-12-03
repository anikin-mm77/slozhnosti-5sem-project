

def st_all_different_solution(graph: list[list[int]]) -> object:
    """
    Принимает на вход граф в виде списка, i-ый элемент которого - список номеров вершин, 
    которые соединены ребром с i-ой вершиной
    
    Ищет как можно меньшее (не оптимальное) количество цветов, 
    в которые можно покрасить все вершины графа так, 
    чтобы ни одно ребро не соединяло одноцветные вершины 

    Возвращает JSON с двумя объектами:
     1. answer - количество цветов для раскраски
     2. answer_expanded - раскраску графа в виде списка, i-ый элемент которого - цвет i-ой вершины
    """

    graph_degree = len(graph)
    colours_in_neighbours = [set() for _ in range(graph_degree)] # какие цвета уже есть у соседей
    answer_expanded = [-1 for i in range(graph_degree)]

    coloured = 0 # сколько вершин покрасили
    while coloured < graph_degree:
        next_vetrex, saturation, deg  = -1, -1, -1

        for v in range(graph_degree):
            if answer_expanded[v] != -1:
                continue
            current_saturation = len(colours_in_neighbours[v])
            if current_saturation > saturation or (current_saturation == saturation and len(graph[v]) > deg):
                next_vetrex, saturation, deg = v, current_saturation, len(graph[v])

        used_colours = colours_in_neighbours[next_vetrex]
        new_vertex_colour = 0
        while new_vertex_colour in used_colours:
            new_vertex_colour += 1
        answer_expanded[next_vetrex] = new_vertex_colour
        coloured += 1

        for u in graph[next_vetrex]:
            if answer_expanded[u] == -1:
                colours_in_neighbours[u].add(new_vertex_colour)

    return {
        "answer": len(set(answer_expanded)),
        "answer_expanded": answer_expanded,
    }