.PHONY: run
run:
	@poetry run chipper roms/PONG 2> output


.PHONY: install-deps
install-deps:
	@poetry install
