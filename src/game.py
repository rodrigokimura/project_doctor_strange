from colorama import Fore, Back, Style

from typing import Tuple, List, Set, Optional
from enum import Enum
import functools


class Color(Enum):
    W = "white"
    Y = "yellow"
    C = "cyan"
    M = "magenta"
    E = "empty"


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
            Color.E: (Back.BLACK, Fore.BLACK),
        }
        return f"{colors[self.color][0]}{colors[self.color][1]}   {Style.RESET_ALL}"

    def __repr__(self) -> str:
        return f"Cell({self.color}, ({self.x +1}, {self.y + 1}))"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Cell):
            return self.color == __o.color
        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    def coords(self) -> Tuple[int, int]:
        return self.x, self.y

    def is_empty(self):
        return self.color == Color.E

    @classmethod
    def empty(cls, x: int, y: int):
        cell = cls(Color.E)
        cell.x, cell.y = x, y
        return cell


class Board:
    def __init__(self, cells: Tuple[Tuple[Cell, ...], ...]) -> None:
        try:
            self.size = len(cells)
            self._cells = [[0 for _ in range(self.size)] for _ in range(self.size)]
            for row in range(self.size):
                for col in range(self.size):
                    cell = cells[row][col]
                    cell.x, cell.y = row, col
                    self._cells[row][col] = cell
        except IndexError:
            raise ValueError("Board must be a square")

    def __str__(self) -> str:
        return "\n".join("".join(str(cell) for cell in row) for row in self._cells)

    def get_cell(self, row: int, col: int) -> Cell:
        return self._cells[row - 1][col - 1]

    def get_col(self, col: int):
        return [self._cells[i][col] for i in range(self.size)]

    def neighbours(self, row: int, col: int) -> List[Cell]:
        rows, cols = {row - 1, row + 1}, {col - 1, col + 1}
        if row == 1:
            rows.remove(row - 1)
        if row == self.size:
            rows.remove(row + 1)
        if col == 1:
            cols.remove(col - 1)
        if col == self.size:
            cols.remove(col + 1)
        neighbours = set()
        for _row in rows:
            neighbours.add(self.get_cell(_row, col))
        for _col in cols:
            neighbours.add(self.get_cell(row, _col))
        del rows
        del cols
        return neighbours

    def get_matching_cells(self, cell: Cell, exclude: Set[Cell]) -> bool:
        matching_cells = {cell}
        for _cell in self.neighbours(cell.x + 1, cell.y + 1):
            if _cell in exclude:
                continue
            if _cell == cell:
                matching_cells.add(cell)
                matching_cells = matching_cells.union(
                    self.get_matching_cells(_cell, exclude.union(matching_cells))
                )
        return matching_cells

    def is_empty(self):
        return all(c.color == Color.E.value for row in self._cells for c in row)


class Game:
    SIZE = 5
    current_move: int = 0
    max_movements: int

    def __init__(self, board: Board, max_movements: int) -> None:
        self.board = board
        self.max_movements = max_movements

    class InvalidCommand(Exception):
        """Invalid command"""

    class NoOpCommand(Exception):
        """Command does nothing"""

    def play(self, inputs: Optional[List[int]] = None):
        while True:
            self.print_board()
            print(f"Movements left: {self.max_movements - self.current_move}")
            if inputs:
                try:
                    self.execute_command(inputs[self.current_move])
                except self.NoOpCommand:
                    pass
            else:
                try:
                    self.execute_command(int(input("Enter position: ")))
                except (ValueError, self.InvalidCommand, self.NoOpCommand):
                    print("Invalid, try again")
                    continue
            self.current_move += 1
            if self.board.is_empty():
                print(
                    Fore.GREEN
                    + f"VICTORY! Finished in {self.current_move} movements."
                    + Style.RESET_ALL
                )
                return True
            if self.current_move >= self.max_movements:
                break
        print(Fore.RED + "GAME OVER!" + Style.RESET_ALL)
        return False

    def print_board(self):
        print(self.board)

    def execute_command(self, position: int):
        if position > self.board.size or position < 0:
            raise self.InvalidCommand
        cell = self.board.get_cell(5, position)
        if cell.is_empty():
            raise self.NoOpCommand
        cells = self.board.get_matching_cells(cell, set())
        self.destroy_cells(cells)

    def destroy_cells(self, cells: Set[Cell]):
        cols = {cell.y for cell in cells}
        for col in cols:
            c = len([c for c in cells if c.y == col])
            new_cells = [c for c in self.board.get_col(col) if c not in cells]
            for i in range(self.board.size):
                if i < c:
                    self.board._cells[i][col] = Cell.empty(i, col)
                else:
                    self.board._cells[i][col] = new_cells[i - c]
                    new_cells[i - c].x = i


if __name__ == "__main__":
    _c = Color
    game = Game(
        board=Board(
            cells=(
                (Cell(_c.W), Cell(_c.Y), Cell(_c.C), Cell(_c.M), Cell(_c.Y)),
                (Cell(_c.Y), Cell(_c.Y), Cell(_c.C), Cell(_c.M), Cell(_c.C)),
                (Cell(_c.W), Cell(_c.W), Cell(_c.Y), Cell(_c.C), Cell(_c.Y)),
                (Cell(_c.Y), Cell(_c.M), Cell(_c.M), Cell(_c.C), Cell(_c.W)),
                (Cell(_c.C), Cell(_c.C), Cell(_c.Y), Cell(_c.M), Cell(_c.W)),
            )
        ),
        max_movements=10,
    )
    game.play()
