#!/bin/sh
python manage.py reset_db --noinput
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
