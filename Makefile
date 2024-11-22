.PHONY: style all ruff style-check

package?=atm_db exchanger_db registration_db

args = `arg="$(filter-out $@,$(MAKECMDGOALS))" && echo $${arg:-${1}}`

all: style

style:
	black $(package)
	isort $(package)

ruff:
	python -m ruff check $(package)

style-check:
	python -m isort $(package)
	python -m black $(package)

lint: ruff style-check
