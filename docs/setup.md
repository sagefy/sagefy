---
layout: default
title: Setup
---

## Local Development

These instructions assume you are using Mac OS X. To set up a staging or production server, please follow `script/provision.sh` instead.

1.  Install tools
    1.  Install [Docker for Mac](https://www.docker.com/docker-mac).
    2.  Install [Homebrew](https://brew.sh/).
    3.  Install node: `brew install node`
    4.  Install dbmate: `brew tap amacneil/dbmate && brew install dbmate`
2.  Grab the code
    1.  Clone the repository: `git clone https://github.com/sagefy/sagefy.git`
    2.  Enter the directory: `cd sagefy`
3.  Start it up
    1. `docker-compose up`
4.  Get some data
    1.  Create database schemas: `npm run dbmate up`
    2.  Create dev data: `npm run dev-data`
5.  Verify
    1.  In your browser, visit `http://localhost:2601/graphiql`, there should be a Graphiql window.
    2.  In your browser, visit `http://localhost/`, the home page should be working.
    3.  Try to sign up for an account.
6.  Watch and rebuild
    1. `npm install && npm start`

## Commands

To shut down local dev:

    docker-compose down

Rebuild the containers (if config change):

    docker-compose up --build

Restart a service manually:

    docker-compose restart [servicename_1]

Access Postgres REPL:

    npm run dbrepl

Run tests:

    npm install && npm test

[Wipe Docker completely](http://bit.ly/2xrbmWb):

    docker rm -f $(docker ps -a -q)
    docker rmi -f $(docker images -q)

Back up database

    # ssh into the server
    ./script/dbbu.sh

Deploy

    # ssh into the server
    ./script/deploy.sh
