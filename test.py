import time

from datetime import datetime, timedelta
from pathlib import Path
from solution import st_all_different_solution


# Критерии решения задачи
TIME_LIMIT_FOR_EACH_TEST = 30 * 60
GRADED_TEST = {
    "data/gc_50_3": 6,
    "data/gc_70_7": 17,
    "data/gc_100_5": 16,
    "data/gc_250_9": 78,
    "data/gc_500_1": 16,
    "data/gc_1000_5": 100,
}


def reading_input(path_to_file_with_input: str) -> list[list[int]]:
    """"
    Принимает на вход путь до файла с данными

    Возвращает граф в виде списка, i-ый элемент которого - список номеров вершин, 
    которые соединены ребром с i-ой вершиной
    """
    path = Path(__file__).resolve().parent / path_to_file_with_input
    with path.open(encoding="utf-8") as f:
        n, m = map(int, f.readline().split())
        graph = [[] for i in range(n)]
        for _ in range(m):
            u, v = map(int, f.readline().split())
            graph[u].append(v)
            graph[v].append(u)

    return graph


def getting_solution(graph: list[list[int]], solution_func: callable) -> object:
    """
    Принимает на вход граф в виде списка, i-ый элемент которого - список номеров вершин, 
    которые соединены ребром с i-ой вершиной

    Возвращает JSON с двумя объектами:
     1. answer - количество цветов для раскраски
     2. answer_expanded - раскраску графа в виде списка, i-ый элемент которого - цвет i-ой вершины
    """

    return solution_func(graph=graph)


def checking_answer(answer: int, answer_expanded: list[int], graph: list[list[int]]) -> bool:
    """
    Принимает на вход:
     1. Ответ на задачу о наименьшей покраске графа
     1. Раскраску графа в виде списка, i-ый элемент которого - цвет i-ой вершины
     3. Граф в виде списка, i-ый элемент которого - список номеров вершин, 
        которые соединены ребром с i-ой вершиной

    Возвращает True, если нет ребер, соединяющих вершины одного цвета, 
    и числовой ответ равен количеству уникальных цветов вершин. 
    Иначе - False
    """
    if answer != len(set(answer_expanded)):
        return False
    
    for v in range(len(graph)):
        for u in range(len(graph[v])):
            if (answer_expanded[v] == answer_expanded[graph[v][u]]):
                return False 

    return True


def testing(path_to_file_with_input: str, baseline_answer: int, time_limit: int, testing_solution: callable) -> str:
    """
    Принимает на вход: 
      1. Относительный путь до файла с тестовыми данными
      2. Ответ, который надо повторить или превзойти
      3. Ограничение на исполнение программы
      4. Функцию, являющуюся решением задачи

    Вовзращает: строку с отчетом о тестировании
    """
    test_graph = reading_input(path_to_file_with_input=path_to_file_with_input)

    start = time.perf_counter()
    result = getting_solution(test_graph, testing_solution)
    elapsed_sec = time.perf_counter() - start

    is_solution_correct = checking_answer(answer=result["answer"], answer_expanded=result["answer_expanded"], graph=test_graph)
    solution_correction_resolution = "Решение корректно" if is_solution_correct else "Решение НЕкорректно"

    is_baseline_pased = result["answer"] <= baseline_answer
    baseline_passed_reolution = "Бейзлайн пройден" if is_baseline_pased else "Бейзлайн НЕ пройден"

    is_time_limit_passed = elapsed_sec <= time_limit
    time_limit_passed_reolution = "TL пройден" if is_time_limit_passed else "TL НЕ пройден"

    lines = []
    lines.append(f"Тестовый файл: {path_to_file_with_input}")
    lines.append(f"Вердикт решения: {solution_correction_resolution}")
    lines.append(f"Время работы: {elapsed_sec/60:.2f} м., TL: {time_limit/60:.2f} м., вердикт: {time_limit_passed_reolution}")
    lines.append(f"Полученный ответ: {result['answer']}, бейзлайн: {baseline_answer}, вердикт: {baseline_passed_reolution}")
    lines.append(f"Найденная раскраска: {result['answer_expanded']}")

    return "\n".join(lines)


def run_test(testing_solution: callable) -> None:
    """
    Принимает на вход функцию, являющуюся решением задачи

    Запускает тесты на всех тестовых файлах из переменной GRADED_TEST и создает файл report.txt с отчетом о тестировании
    """
    ts = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    header = f"[{ts}] Отчет о тестировании:"
    sections = [header]

    for key, value in GRADED_TEST.items():
        result = testing(path_to_file_with_input=key, baseline_answer=value, time_limit=TIME_LIMIT_FOR_EACH_TEST, testing_solution=testing_solution)
        sections.append(result)

    report_path = f"report.txt"
    path = Path(report_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n\n\n".join(sections), encoding="utf-8")


if __name__ == "__main__":
    run_test(st_all_different_solution)
