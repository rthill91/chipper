.PHONY: run
run: install-deps
	@poetry run chipper


.PHONY: install-deps
install-deps:
	@poetry install
