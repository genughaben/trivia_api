 
## Setup database

> docker exec -it company_data psql -U company_data
> CREATE DATABASE triviadb;
> export FLASK_APP=flaskr
> export FLASK_ENV=development
> flask db upgrade
> docker exec -i company_data psql -U company_data -d triviadb < trivia_content.psql