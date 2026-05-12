.PHONY: run

install:
	@uv sync --all-packages --dev --group test
	@uv run pre-commit install --install-hooks -t pre-commit -t post-checkout -t post-merge -t post-rewrite

clean:
	@uv cache clean
	@uv cache clean ruff
	@uv cache prune
	@uv run pre-commit clean
	@uv run pre-commit gc

lint:
	@uv run pre-commit run --all-files

update:
	uv lock --upgrade
	uv sync --all-packages --dev --group test
	uv run pre-commit autoupdate

test:
	@uv run coverage run -m pytest
	@uv run coverage report
	@uv run coverage html --directory coverage/html

run:
	streamlit run app.py
