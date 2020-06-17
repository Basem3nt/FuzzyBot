web: python manage.py collectstatic
release: python manage.py migrate
web: gunicorn FuzzyBot.wsgi --log-file -