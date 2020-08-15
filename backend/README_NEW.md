# Trivia API instructions:

## Setup database

> docker exec -it company_data psql -U company_data
> CREATE DATABASE triviadb;
> export FLASK_APP=flaskr
> export FLASK_ENV=development
> flask db upgrade
> docker exec -i company_data psql -U company_data -d triviadb < trivia_content.psql

## Run API app:

To execute the API app in DEBUG mode, run:

> FLASK_APP=flaskr/__init__.py FLASK_ENV=development FLASK_DEBUG=1 flask run

NB: debug mode e.g. automatically restarts the app, when code changes occur.

To execute the API app in production mode, run:

> FLASK_APP=flaskr/__init__.py FLASK_ENV=development flask run

## Testing

To execute tests run:

> pytest

## Coverage

To create a coverage report, run:

> coverage html

To view the created report, go to foldeR: htmlcov and open index.html in your favorite browser.