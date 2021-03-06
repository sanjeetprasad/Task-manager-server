#!/bin/bash
rm -rf taskorgapi/migrations
rm db.sqlite3
python3 manage.py migrate
python3 manage.py makemigrations taskorgapi
python3 manage.py migrate taskorgapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata categories
python3 manage.py loaddata tasks
python3 manage.py loaddata tags
python3 manage.py loaddata tasktags
