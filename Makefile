run:
	@uvicorn store.main:app --reload

precommit-install:
	@poetry run pre-commit install

teste:
	@poetry run pytest