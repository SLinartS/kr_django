start:
	python manage.py runserver 8700
mkmigrate:
	python manage.py makemigrations
migrate:
	python manage.py migrate
pipinstall:
	pip install -r requirements.txt
