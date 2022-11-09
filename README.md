# Project Doctor Strange

## Installation

This project uses Pipenv as package manager.

Install pipenv:

```bash
pip install pipenv
```

then use it to install this project's dependencies:

```bash
pipenv install
```

## Usage

For now, this project has two modules:
- game.py
- simulator.py

### game.py

This module replicates the same logic used in the figure.game web browser game.  
By running the module as script you can interactively run a preset version of the game.

```bash
make play
```

### game.py

This module implements different approaches for solving the game.  
As well as the game.py module, you can run this module as script to run one of the implementations.

```bash
make simulate
```

## Inspiration

We came up with the idea in a bar conversation - we thought it would be fun to automate the solution for this game.