#!/bin/bash

python manage.py collectstatic
python manage.py migrate && gunicorn config.wsgi:application -b 0.0.0.0:8000
