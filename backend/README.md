# Trivia API instructions:

## Requirements:
* Python 3.8 Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

## Getting started - Code, Virtualenv and PIP dependencies

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
You can review all required dependenices in the requirements.txt.

> git clone git@github.com:genughaben/trivia_api.git
> python -m venv venv
> pip install -r requirements.txt

## Setup database

### Setup and run postgresql database management system in docker:

> docker-compose up

### Add production database:

> docker exec -it trivia_dbms psql -U postgres
> CREATE DATABASE triviadb;
> \q
> export FLASK_APP=flaskr
> export FLASK_ENV=development
> flask db init
> flask db migrate
> flask db upgrade
> docker exec -i trivia_dbms psql -U postgres -d triviadb < trivia_content.psql

### Add testing database:

> docker exec -it trivia_dbms psql -U postgres
> CREATE DATABASE trivia_test;
> \q
> docker exec -i trivia_dbms psql -U postgres -d trivia_test < trivia.psql
> docker exec -it trivia_dbms psql -U postgres
> \c trivia_test
> ALTER TABLE questions RENAME category TO category_id


## Run API app:

To execute the API app in DEBUG mode, run:

> FLASK_APP=flaskr/__init__.py FLASK_ENV=development flask run

NB: Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

To execute the API app in production mode, run:

> FLASK_APP=flaskr/__init__.py flask run

## Testing

### Automatic Testing:

To execute all tests run:

> pytest

If you want to run individual tests, go into the tests folder and look for INSPECTION section in the test comments.
There are commands to execute individual tests. Adapt those to your liking, if applicable.

### Manual Testing

To inspect the endpoints when of an running app, you can use the import and use the postman collection provided in the file:

backend/trivia.postman_collection.json

## Coverage

To create a coverage report, run:
The required configuration can be found in setup.cfg.

> coverage run -m pytest
> coverage html

To view the created report, go to foldeR: htmlcov and open index.html in your favorite browser.

## Debugging / Logging

For debugging, a log file can be visited to see full error messages and stack trace.
trivia.log.

You can also add more log statements by importing the logger from flaskr/logger.py add write to it using:
* logger.info for info
* logger.debug for debug info
* logger.info error for error info

To read more, look here: https://docs.python.org/3/howto/logging.html

## Endpoints:

This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```
