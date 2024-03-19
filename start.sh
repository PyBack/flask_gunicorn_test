#/bin/sh

gunicorn --workers=2 --bind 0.0.0.0:5500 src.wsgi:app