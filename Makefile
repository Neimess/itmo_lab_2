PATH_TASK_1 = artifacts/task_1
PATH_TASK_2 = artifacts/task_2

all: fmt_linter check_types pytests clear

fmt_linter:
	uv run ruff check --select I --fix .
	uv run ruff format . --no-cache
	@echo '[OK] Formatters went through successfully'
	uv run ruff check . --no-cache --fix
	@echo '[OK] Linters checks passed successfully'

check_types:
	mypy src

pytests:
	uv run pytest tests -vv -s

clear:
	rm -f ${PATH_TASK_1}/*.tex ${PATH_TASK_1}/*.pdf ${PATH_TASK_1}/*.log ${PATH_TASK_1}/*.aux
	rm -f ${PATH_TASK_2}/*.tex ${PATH_TASK_2}/*.pdf ${PATH_TASK_2}/*.log ${PATH_TASK_2}/*.aux
