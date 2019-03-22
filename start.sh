#!/bin/bash

echo "testeroni mit em toni"
cd /opt/mate_counter
python manage.py migrate
python manage.py runserver
