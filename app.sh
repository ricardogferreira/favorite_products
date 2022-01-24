#!/bin/sh
echo "WAIT POSTGRESQL"
bash /usr/wait-for-it.sh postgres:5432

echo "MIGRATING"
flask db upgrade

echo "RUNNING"
flask run --host=0.0.0.0
