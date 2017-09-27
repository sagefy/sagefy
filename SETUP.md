Setup
=====

Local Development
-----------------

These instructions assume you are using Mac OS X.

1. Install [Docker for Mac](https://www.docker.com/docker-mac).
2. Clone the Repository: `git clone https://github.com/heiskr/sagefy.git`
3. Enter the directory: `cd sagefy`
3. `cp server/config.dev.example.py server/config.py`
4. `docker-compose up -d`
5. Create database schemas (when first time):
    - `docker exec -it sagefy_postgres_1 psql -U sagefy -a -f /www/sagefy_tables.sql`
    - `docker exec -it sagefy_postgres-test_1 psql -U test -a -f /www/sagefy_tables.sql`
6. Create Dev Data: `docker-compose run server python /www/dev_data.py`
7. In your browser, visit `http://localhost/s/`, there should be a welcome message.
8. In your browser, visit `http://localhost/`, the home page should be working. Try to sign up for an account.
9. Run watchers: `npm install && npm start`

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

    docker-compose run server coverage run --module py.test
    docker-compose run server coverage report --omit="test/*"

Run client tests:

    docker-compose run client npm test

[Wipe Docker completely](http://bit.ly/2xrbmWb):

    docker rm -f $(docker ps -a -q)
    docker rmi -f $(docker images -q)

Deploy steps
------------

TODO Update these to use docker-compose. (npm deploy, database backup before deploy!)

    ++ ssh into the server ++
    cd /var/www
    sudo git pull origin master
    cd client
    sudo npm run deploy
    sudo cp -a app/images/* distribution/ && sudo cp -a app/*.{html,txt,ico} distribution/
    pm2 restart all

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

TODO update these to scripts and docker-compose
TODO Set up as a cron job... fix the environment :)
