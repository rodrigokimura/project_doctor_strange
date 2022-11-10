from enum import Enum
from typing import Dict, List, Optional, Set, Tuple

from colorama import Back, Fore, Style


class Color(Enum):
    W = "white"
    Y = "yellow"
    C = "cyan"
    M = "magenta"
    E = "empty"


class Cell:
    color: Color

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
        return f"Cell({self.color})"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Cell):
            return self.color == __o.color
        return False

    def is_empty(self):
        return self.color == Color.E

    @classmethod
    def empty(cls):
        return cls(Color.E)


class Board:
    cells: Dict[Tuple[int, int], Cell] = {}

    def __init__(self, cells: Tuple[Tuple[Cell, ...], ...]) -> None:
        try:
            self.size = len(cells)
            for row in range(self.size):
                for col in range(self.size):
                    cell = cells[row][col]
                    self.cells[(row, col)] = cell
        except IndexError:
            raise ValueError("Board must be a square")

    def __str__(self) -> str:
        return "\n".join(
            "".join(str(self.cells[(row, col)]) for col in range(self.size))
            for row in range(self.size)
        )

    def get_cell(self, row: int, col: int) -> Cell:
        return self.cells[(row, col)]

    def get_col(self, col: int):
        return ((i, col) for i in range(self.size))

    def get_neighbours(self, row: int, col: int) -> List[Cell]:
        rows, cols = {row - 1, row + 1}, {col - 1, col + 1}
        if row == 0:
            rows.remove(row - 1)
        if row == self.size - 1:
            rows.remove(row + 1)
        if col == 0:
            cols.remove(col - 1)
        if col == self.size - 1:
            cols.remove(col + 1)
        neighbours = set()
        for _row in rows:
            neighbours.add((_row, col))
        for _col in cols:
            neighbours.add((row, _col))
        return neighbours

    def get_matching_cells(
        self, coords: Tuple[int, int], exclude: Set[Tuple[int, int]]
    ) -> bool:
        matching_cells = {coords}
        for _coords in self.get_neighbours(*coords):
            if _coords in exclude:
                continue
            if self.get_cell(*_coords) == self.get_cell(*coords):
                matching_cells.add(coords)
                matching_cells = matching_cells.union(
                    self.get_matching_cells(_coords, exclude.union(matching_cells))
                )
        return matching_cells

    def is_empty(self):
        return all(c.color == Color.E for c in self.cells.values())

    def count_remaining_cells(self):
        return len([c for c in self.cells.values() if not c.is_empty()])


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

    def play(self):
        while True:
            self.print_board()
            print(f"Movements left: {self.max_movements - self.current_move}")
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

    def run_sequence(self, inputs: Optional[List[int]] = None):
        while True:
            try:
                self.execute_command(inputs[self.current_move])
            except self.NoOpCommand:
                pass
            self.current_move += 1
            if self.board.is_empty():
                return True
            if self.current_move >= self.max_movements:
                break
        return False

    def print_board(self):
        print(self.board)

    def execute_command(self, position: int):
        if position > self.board.size or position <= 0:
            raise self.InvalidCommand
        cell = self.board.get_cell(4, position - 1)
        if cell.is_empty():
            raise self.NoOpCommand
        cell_coords_to_destroy = self.board.get_matching_cells((4, position - 1), set())
        self.destroy_cells(cell_coords_to_destroy)

    def destroy_cells(self, coords: Set[Tuple[int, int]]):
        cols = {coord[1] for coord in coords}
        for col in cols:
            cells_to_destroy = len([c for c in coords if c[1] == col])
            new_cells = [
                self.board.get_cell(row, col)
                for row in range(self.board.size)
                if (row, col) not in coords
            ]
            for row in range(self.board.size):
                self.board.cells[(row, col)] = (
                    Cell.empty()
                    if row < cells_to_destroy
                    else new_cells[row - cells_to_destroy]
                )


if __name__ == "__main__":
    _c = Color
    # possible solution: 143521421
    game = Game(
        board=Board(
            cells=(
                (Cell(_c.C), Cell(_c.W), Cell(_c.Y), Cell(_c.M), Cell(_c.M)),
                (Cell(_c.Y), Cell(_c.Y), Cell(_c.Y), Cell(_c.Y), Cell(_c.Y)),
                (Cell(_c.W), Cell(_c.M), Cell(_c.M), Cell(_c.M), Cell(_c.C)),
                (Cell(_c.Y), Cell(_c.W), Cell(_c.M), Cell(_c.C), Cell(_c.M)),
                (Cell(_c.C), Cell(_c.W), Cell(_c.M), Cell(_c.W), Cell(_c.C)),
            )
        ),
        max_movements=9,
    )
    game.play()
