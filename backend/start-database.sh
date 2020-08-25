#!/bin/bash
set -u

# checks if trivia_dbms has been created and is running, and stops it
if docker ps | grep -q trivia_dbms
then
  echo "stopping already existing trivia_dbms"
  docker stop trivia_dbms
fi

# checks if trivia_dbms has been created and is stopped, and removes it
if docker ps -aq -f status=exited -f name=trivia_dbms
then
  echo "removing already existing trivia_dbms"
  docker rm trivia_dbms
fi

# (re-)create trivia_dbms from docker-compose.yml
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
