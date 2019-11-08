pip install -r requirements-dev.txt
pytest --cov=pyoracle_forms tests/
coverage-badge -o media/coverage.svg -f