from src.game import Game, Board, Cell, Color


def test_sim():
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
    game.board.get_matching_cells(3)
