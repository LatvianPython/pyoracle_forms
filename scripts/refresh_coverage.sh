pip install -r requirements-test.txt
pytest --cov=pyoracle_forms tests/
coverage-badge -o media/coverage.svg -f