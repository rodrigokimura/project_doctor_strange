from itertools import product
from typing import List, Tuple

from game import Board, Cell, Color, Game


class Simulator:
    successful_sequences: List[Tuple[int, ...]]

    def __init__(self, initial_cells: Tuple[Tuple[Cell, ...], ...]):
        self.initial_cells = initial_cells
        self.successful_sequences = []

    def run(self):
        MAX_MOVEMENTS = 10
        POSITIONS = len(self.initial_cells)
        total_combinations = POSITIONS**MAX_MOVEMENTS
        for i, inputs in enumerate(product(*[range(1, POSITIONS + 1)] * MAX_MOVEMENTS)):
            progress = i / total_combinations
            print(f"Progress: {progress:.2%}")
            game = Game(
                board=Board(cells=self.initial_cells),
                max_movements=MAX_MOVEMENTS,
            )
            victory = game.run_inputs(inputs)
            if victory:
                self.successful_sequences.append(inputs)
        print(f"Victorious possibilities found: {len(self.successful_sequences)}")
        for seq in self.successful_sequences:
            print(seq)


if __name__ == "__main__":
    _c = Color
    simulator = Simulator(
        initial_cells=(
            (Cell(_c.W), Cell(_c.Y), Cell(_c.C), Cell(_c.M), Cell(_c.Y)),
            (Cell(_c.Y), Cell(_c.Y), Cell(_c.C), Cell(_c.M), Cell(_c.C)),
            (Cell(_c.W), Cell(_c.W), Cell(_c.Y), Cell(_c.C), Cell(_c.Y)),
            (Cell(_c.Y), Cell(_c.M), Cell(_c.M), Cell(_c.C), Cell(_c.W)),
            (Cell(_c.C), Cell(_c.C), Cell(_c.Y), Cell(_c.M), Cell(_c.W)),
        ),
    )
    simulator.run()
