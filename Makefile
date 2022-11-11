export PYTHONPATH := 'scr'

lint:
	@pipenv run black .
	@pipenv run isort .

play:
	@pipenv run python src/game.py

simulate:
	@pipenv run python src/simulator.py

qa:
	@pipenv run pytest
