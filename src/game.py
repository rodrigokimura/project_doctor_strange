from colorama import Fore, Back, Style

from enum import Enum
import functools


class Color(Enum):
    W = "white"
    Y = "yellow"
    C = "cyan"
    M = "magenta"


class Cell:
    color: Color
    x: int
    y: int

    def __init__(self, color: Color) -> None:
        self.color = color

    def __str__(self) -> str:
        colors = {
            Color.W: (Back.WHITE, Fore.BLACK),
            Color.Y: (Back.YELLOW, Fore.BLACK),
            Color.C: (Back.CYAN, Fore.BLACK),
            Color.M: (Back.MAGENTA, Fore.BLACK),
        }
        return f"{colors[self.color][0]}{colors[self.color][1]} {self.color.value[0]} {Style.RESET_ALL}"

    def __repr__(self) -> str:
        return f"Cell({self.color})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Cell):
            return self.color == __o.color
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    def coords(self) -> tuple[int, int]:
        return self.x, self.y


class Board:
    size = 5

    def __init__(self, cells: tuple[tuple[Cell, ...], ...]) -> None:
        try:
            self._cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
            for row in range(self.size):
                for col in range(self.size):
                    cell = cells[row][col]
                    cell.x, cell.y = row, col
                    self._cells[row][col] = cell
        except IndexError:
            raise ValueError(f"Board must be {self.size}x{self.size}")

    def __str__(self) -> str:
        return "\n".join("".join(str(cell) for cell in row) for row in self._cells)

    def get_cell(self, row: int, col: int) -> Cell:
        return self._cells[row - 1][col - 1]

    def neighbours(self, row: int, col: int) -> list[Cell]:
        rows, cols = {row - 1, row + 1}, {col - 1, col + 1}
        if row == 1:
            rows.remove(row - 1)
        if row == self.size:
            rows.remove(row + 1)
        if col == 1:
            cols.remove(col - 1)
        if col == self.size:
            cols.remove(col + 1)
        for row in rows:
            for col in cols:
                yield self.get_cell(row, col)

    def get_matching_neighbours(self, cell: Cell) -> list[Cell]:
        return [
            neighbour
            for neighbour in self.neighbours(*cell.coords)
            if neighbour == cell
        ]

    @functools.lru_cache
    def get_matching_cells(self, cell: Cell, exclude: list[Cell]) -> bool:
        matching_cells = {cell}
        for _cell in self.neighbours(cell.x + 1, cell.y + 1):
            if _cell in exclude:
                continue
            if _cell == cell:
                matching_cells.add(cell)
            matching_cells.union(self.get_matching_cells(_cell, matching_cells))
        return matching_cells


class Game:
    SIZE = 5

    def __init__(self, board: Board) -> None:
        self.board = board

    def select_cell(x):
        pass

    def print_board(self):
        print(self.board)


if __name__ == "__main__":
    board = Board(
        cells=(
            (Cell(Color.W), Cell(Color.Y), Cell(Color.C), Cell(Color.M), Cell(Color.Y)),
            (Cell(Color.Y), Cell(Color.Y), Cell(Color.C), Cell(Color.M), Cell(Color.C)),
            (Cell(Color.W), Cell(Color.W), Cell(Color.Y), Cell(Color.C), Cell(Color.Y)),
            (Cell(Color.Y), Cell(Color.M), Cell(Color.M), Cell(Color.C), Cell(Color.W)),
            (Cell(Color.C), Cell(Color.C), Cell(Color.Y), Cell(Color.M), Cell(Color.W)),
        )
    )
    game = Game(board)
    game.print_board()
    cell = game.board.get_cell(5, 1)
    print(cell)
    cells = game.board.get_matching_cells(cell, [cell])
    print(cells)
