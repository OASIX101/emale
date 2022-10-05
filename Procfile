web: gunicorn -b "0.0.0.0:$PORT" -w 3 home_vote.wsgi
release: python manage.py migrate