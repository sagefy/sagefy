Setup
=====

Local Development
-----------------

These instructions assume you are using Mac OS X.

1. Install tools
    1. Install [Docker for Mac](https://www.docker.com/docker-mac).
    2. Install [Homebrew](https://brew.sh/).
    3. Install yarn: `brew install yarn`
2. Grab the code
    1. Clone the repository: `git clone https://github.com/heiskr/sagefy.git`
    2. Enter the directory: `cd sagefy`
    3. `cp server/config.dev.example.py server/config.py`
3. Start it up: `docker-compose up -d`
4. Get some data
    1. Create database schemas (when first time):
        - `docker exec -it sagefy_postgres_1 psql -U sagefy -a -f /www/sagefy_tables.sql`
        - `docker exec -it sagefy_postgres-test_1 psql -U test -a -f /www/sagefy_tables.sql`
    2. Create dev data: `docker-compose run server python /www/test/dev_data.py`
5. Verify
    1. In your browser, visit `http://localhost/s/`, there should be a welcome message.
    2. In your browser, visit `http://localhost/`, the home page should be working.
    3. Try to sign up for an account.
6. Watch and rebuild: `yarn install && yarn start`

Some Useful Commands
--------------------

To shut down local dev:

    docker-compose down --remove-orphans

Watch the local dev logs:

    docker-compose logs --follow

Rebuild the containers (if config change):

    docker-compose up --build -d

Restart a service manually:

    docker-compose restart [servicename_1]

Access Postgres REPL:

    docker exec -it sagefy_postgres_1 psql -U sagefy

Run server tests:

    docker-compose run server flake8
    docker-compose run server coverage run --module py.test
    docker-compose run server coverage report --omit="test/*"

Run client tests:

    docker-compose run client yarn test

[Wipe Docker completely](http://bit.ly/2xrbmWb):

    docker rm -f $(docker ps -a -q)
    docker rmi -f $(docker images -q)

Deploy steps
------------

How to deploy the latest master:

    ++ ssh into the server ++
    cd /var/www
    ++ back up the database ++
    git pull origin master
    docker-compose run client yarn run deploy
    docker-compose restart server
    docker-compose restart client

Things to fix:

- The server should not know about git
- Fix permissions so we don't have to run `cp` by itself.
- We should need to restart uwsgi, which should not be in watch mode on prod.

Back up the database
--------------------

Run:

    ++ ssh into the server ++
    cd /var/www/dbbu
    today=`date '+%Y_%m_%d__%H_%M_%S'`
    sudo -u postgres pg_dump sagefy > "sagefy-$today.sql"
    b2 authorize_account xxx xxxxxxxx  # see dashlane
    b2 sync /var/www/dbbu b2:sagefy-dbbu

TODO update these to scripts to docker-compose
TODO Set up as a cron job... fix the environment :)
