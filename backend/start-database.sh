#!/bin/bash
set -u

docker-compose up -d --force-recreate
sleep 10

# creates triviadb and trivia_test dbs;
docker exec -i trivia_dbms psql -U postgres < init.sql

# inits, migrates and upgrades db schema using Flask-Migrate
source venv/bin/activate
export FLASK_APP=flaskr
export FLASK_ENV=development
flask db init
flask db migrate
flask db upgrade

# seed production database
docker exec -i trivia_dbms psql -U postgres -d triviadb < trivia_content.psql

# seed testing database
docker exec -i trivia_dbms psql -U postgres -d trivia_test < trivia.psql
docker exec -i trivia_dbms psql -U postgres -d trivia_test -c "ALTER TABLE questions RENAME category TO category_id"
