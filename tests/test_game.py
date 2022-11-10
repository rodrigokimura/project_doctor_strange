import pytest
from colorama import Back, Fore, Style

from src.game import Board, Cell, Color


class TestCell:
    @pytest.fixture
    def cell(self):
        return Cell(Color.C)

    @pytest.fixture
    def empty_cell(self):
        return Cell(Color.E)

    def test_cells_equality(self, cell: Cell):
        assert cell == Cell(Color.C)
        assert cell != Cell(Color.E)

    def test_empty_cell_is_empty(self, empty_cell: Cell):
        assert empty_cell.is_empty()

    def test_filled_cell_is_not_empty(self, cell: Cell):
        assert cell.is_empty() is False

    def test_empty_cell_factory(self, empty_cell: Cell):
        assert Cell.empty() == empty_cell
        assert Cell.empty().is_empty()

    def test_cell_color_display(self, cell: Cell):
        assert str(cell) == f"{Back.CYAN}{Fore.BLACK}   {Style.RESET_ALL}"


class TestBoard:
    @pytest.fixture
    def board(self):
        _c = Color
        return Board(
            cells=(
                (Cell(_c.C), Cell(_c.W), Cell(_c.Y), Cell(_c.M), Cell(_c.M)),
                (Cell(_c.Y), Cell(_c.Y), Cell(_c.Y), Cell(_c.Y), Cell(_c.Y)),
                (Cell(_c.W), Cell(_c.M), Cell(_c.M), Cell(_c.M), Cell(_c.C)),
                (Cell(_c.Y), Cell(_c.W), Cell(_c.M), Cell(_c.C), Cell(_c.M)),
                (Cell(_c.C), Cell(_c.W), Cell(_c.M), Cell(_c.W), Cell(_c.C)),
            )
        )

    @pytest.fixture
    def empty_board(self):
        _c = Color
        return Board(
            cells=tuple(tuple(Cell(_c.E) for _ in range(5)) for _ in range(5)),
        )

    def test_get_cell(self, board: Board):
        cell = board.get_cell(0, 2)
        assert cell.color == Color.Y

    def test_neighbours(self, board: Board):
        neighbours = board.get_neighbours(0, 2)
        assert neighbours == {(0, 1), (0, 3), (1, 2)}

    def test_get_matching_cells(self, board: Board):
        matching_cells = board.get_matching_cells((0, 2), set())
        assert matching_cells == {(0, 2), (1, 2), (1, 0), (1, 1), (1, 3), (1, 4)}

    def test_is_not_empty(self, board: Board):
        assert board.is_empty() is False

    def test_is_empty(self, empty_board: Board):
        assert empty_board.is_empty() is True

    def test_count_remaining_cells(self, board: Board):
        assert board.count_remaining_cells() == 25

    def test_count_remaining_cells_empty_board(self, empty_board: Board):
        assert empty_board.count_remaining_cells() == 0
