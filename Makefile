export PYTHONPATH := 'scr'

lint:
	@pipenv run black .

run:
	@pipenv run python src/game.py