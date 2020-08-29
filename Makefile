GAME=CONNECT4


.PHONY: run
run:
	@poetry run chipper roms/${GAME} 2> output


.PHONY: install-deps
install-deps:
	@poetry install
