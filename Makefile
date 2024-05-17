############### virtualenv
-include .env

venv: venv/touchfile

venv/touchfile: requirements.txt
	test -d venv || python3 -m venv venv
	touch venv/touchfile

############### install

.PHONY: install
install: venv install-pre-commit
	. venv/bin/activate; make install-deps

.PHONY: install-pre-commit
install-pre-commit:
	mkdir -p .git/hooks
	echo "#!/bin/bash\nmake lint" > .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

.PHONY: install-deps
install-deps:
	pip install -r requirements.txt


############### migrate

.PHONY: migrate
migrate: venv
	. venv/bin/activate; alembic upgrade head

.PHONY: create-migration
create-migration:
	. venv/bin/activate; alembic revision --autogenerate -m "$(shell date +%s)"
	make format
	git add migrations