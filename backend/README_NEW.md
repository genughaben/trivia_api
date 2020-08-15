# Trivia API instructions:

## Debugging / Logging

For debugging, a log file can be visited to see full error messages and stack trace.
trivia.log.

You can also add more log statements by importing the logger from flaskr/logger.py add write to it using:
* logger.info for info
* logger.debug for debug info
* logger.info error for error info

To read more, look here: https://docs.python.org/3/howto/logging.html

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