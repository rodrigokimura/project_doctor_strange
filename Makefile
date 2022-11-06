export PYTHONPATH := 'scr'

lint:
	@pipenv run black .

play:
	@pipenv run python src/game.py

simulate:
	@pipenv run python src/simulator.py