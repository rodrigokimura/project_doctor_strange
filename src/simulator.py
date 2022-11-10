import asyncio
import random
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
            victory = game.run_sequence(inputs)
            if victory:
                self.successful_sequences.append(inputs)
        print(f"Victorious possibilities found: {len(self.successful_sequences)}")
        for seq in self.successful_sequences:
            print(seq)


class AsyncIOSimulator:
    successful_sequences: List[Tuple[int, ...]]

    def __init__(self, initial_cells: Tuple[Tuple[Cell, ...], ...]):
        self.initial_cells = initial_cells
        self.successful_sequences = []

    async def run(self):
        MAX_MOVEMENTS = 10
        POSITIONS = len(self.initial_cells)
        total_combinations = POSITIONS**MAX_MOVEMENTS
        tasks = []
        for i, inputs in enumerate(product(*[range(1, POSITIONS + 1)] * MAX_MOVEMENTS)):
            progress = i / total_combinations
            print(f"Task queueing progress: {progress:.2%}")
            tasks.append(
                run_simulation(
                    self.initial_cells, MAX_MOVEMENTS, inputs, self.successful_sequences
                )
            )
            if i == total_combinations - 1:
                await asyncio.gather(*tasks)

            if len(tasks) == 1000000:
                await asyncio.gather(*tasks)
                tasks = []
        print(f"Victorious possibilities found: {len(self.successful_sequences)}")
        for seq in self.successful_sequences:
            print(seq)


class GeneticSimulator:
    max_iterations = 1000
    population_size = 100
    population = {}
    mutation_rate = 1
    selection_threshold = 50

    def __init__(self, initial_cells: Tuple[Tuple[Cell, ...], ...]):
        self.initial_cells = initial_cells

    def run(self):
        self.generate_initial_population()
        for i in range(self.max_iterations):
            print(f"Iteration {i}")
            if solution := self.get_solution():
                print("Solution found!")
                print(solution)
                return
            self.generate_next_population()
        print(f"No solution found after {self.max_iterations} iterations")

    def generate_initial_population(self):
        for _ in range(self.population_size):
            inputs = tuple(random.randint(1, 5) for _ in range(10))
            self.population[inputs] = self.run_game(inputs)

    def run_game(self, inputs):
        game = Game(
            board=Board(cells=self.initial_cells),
            max_movements=10,
        )
        game.run_sequence(inputs)
        return game.board.count_remaining_cells()

    def get_solution(self):
        for k, v in self.population.items():
            if v == 0:
                return k

    def generate_next_population(self):
        parents = self.get_best_parents(self.selection_threshold)
        worst_parents = self.get_worst_parents(self.selection_threshold)
        children = self.generate_children(parents)
        for p in worst_parents:
            self.population.pop(p)
        for c in children:
            self.population[c] = self.run_game(c)

    def get_best_parents(self, couples):
        return tuple(
            k
            for k, _ in sorted(self.population.items(), key=lambda x: x[1])[
                : (2 * couples)
            ]
        )

    def get_worst_parents(self, couples):
        return tuple(
            k
            for k, _ in sorted(self.population.items(), key=lambda x: -x[1])[
                : (2 * couples)
            ]
        )

    def generate_children(self, parents):
        all_children = []
        for i in range(len(parents) // 2):
            parent_1 = parents[i]
            parent_2 = parents[-(i + 1)]
            children = (
                parent_1[:5] + parent_2[5:],
                parent_1[5:] + parent_2[:5],
            )
            if random.random() < self.mutation_rate:
                children = (
                    self.mutate(children[0]),
                    self.mutate(children[1]),
                )
            all_children.extend(children)
        return all_children

    def mutate(self, inputs):
        return tuple(random.randint(1, 5) for _ in range(10))


async def run_simulation(
    cells: Tuple[Tuple[Cell, ...], ...],
    max_movements: int,
    inputs: Tuple[int, ...],
    successful_sequences: List[Tuple[int, ...]],
):
    game = Game(
        board=Board(cells=cells),
        max_movements=max_movements,
    )
    victory = game.run_sequence(inputs)
    if victory:
        successful_sequences.append(inputs)
    print(".", end="", flush=True)


if __name__ == "__main__":
    _c = Color
    simulator = GeneticSimulator(
        initial_cells=(
            (Cell(_c.W), Cell(_c.Y), Cell(_c.W), Cell(_c.M), Cell(_c.W)),
            (Cell(_c.M), Cell(_c.W), Cell(_c.W), Cell(_c.M), Cell(_c.Y)),
            (Cell(_c.Y), Cell(_c.M), Cell(_c.Y), Cell(_c.W), Cell(_c.Y)),
            (Cell(_c.Y), Cell(_c.M), Cell(_c.W), Cell(_c.M), Cell(_c.W)),
            (Cell(_c.W), Cell(_c.W), Cell(_c.C), Cell(_c.Y), Cell(_c.M)),
        ),
    )
    simulator.run()
