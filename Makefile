start:
	python manage.py runserver 8700

migratemk:
	python manage.py makemigrations

migrate:
	python manage.py migrate

mkenv:
	python -m venv .venv

rinstall:
	pip3 install -r requirements.txt

seed:
	python .\manage.py loaddata role.yaml && \
	python .\manage.py loaddata user.yaml && \
	python .\manage.py loaddata filetype.yaml && \
	python .\manage.py loaddata groups.yaml && \
	python .\manage.py loaddata access_code.yaml

