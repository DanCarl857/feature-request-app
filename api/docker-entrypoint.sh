#!/bin/sh

python migrate.py db init
python migrate.py db migrate
python migrate.py db upgrate

cd /api
python run.py