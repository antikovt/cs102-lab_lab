import random
from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd

cur_step = (0, 0)


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    if x == 1 and y != len(grid[0])-2:
        grid[x][y+1] = ' '
    elif y == len(grid[0])-2 and x != 1:
        grid[x-1][y] = ' '
    elif x != 1 and y != len(grid[0])-2:
        wall = random.choice((0, 1))
        if wall == 0:
            grid[x-1][y] = ' '
        else:
            grid[x][y+1] = ' '
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    for coord in empty_cells:
        grid = remove_wall(grid, coord)

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []

    for i in range(len(grid[0])):
        if grid[0][i] == 'X':
            exits.append((0, i))
        if grid[-1][i] == 'X':
            exits.append((len(grid)-1, i))

    for j in range(1, len(grid)-1):
        if grid[j][0] == 'X':
            exits.append((j, 0))
        if grid[j][-1] == 'X':
            exits.append((j, len(grid[0])-1))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k:
                if i+1 < len(grid) and grid[i+1][j] == 0:
                    grid[i+1][j] = k + 1
                if i-1 >= 0 and grid[i-1][j] == 0:
                    grid[i-1][j] = k + 1
                if j+1 < len(grid[0]) and grid[i][j+1] == 0:
                    grid[i][j+1] = k + 1
                if j-1 >= 0 and grid[i][j-1] == 0:
                    grid[i][j-1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    a, b = exit_coord
    path = [(a, b)]
    while grid[a][b] != 1:
        num = grid[a][b] - 1
        if a+1 < len(grid) and grid[a+1][b] == num:
            a += 1
        elif a-1 >= 0 and grid[a-1][b] == num:
            a -= 1
        elif b+1 < len(grid[0]) and grid[a][b+1] == num:
            b += 1
        elif b-1 >= 0 and grid[a][b-1] == num:
            b -= 1
        path.append((a, b))
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    if grid[x-1][y] in ("X", "■") \
            and grid[x][y-1] in ("X", "■") \
            and (x+1 < len(grid) and grid[x+1][y] in ("X", "■")) \
            and (y+1 < len(grid[0]) and grid[x][y+1] in ("X", "■")):
        return True
    else:
        return False


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)
    if len(exits) == 1:
        return grid, exits
    if encircled_exit(grid, exits[0]) is True or encircled_exit(grid, exits[1]) is True:
        return grid, None

    x, y = exits[0]
    z, w = exits[1]
    grid[x][y] = 1
    grid[z][w] = 0
    k = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " ":
                grid[i][j] = 0

    while grid[z][w] == 0:
        k += 1
        grid = make_step(grid, k)

    path = shortest_path(grid, (z, w))

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
                if type(grid[i][j]) == int:
                    grid[i][j] = " "
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
