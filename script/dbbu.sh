#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs -d '\n')
cd /var/sagefy/dbbu
rm *
today=`date '+%Y_%m_%d__%H_%M_%S'`
docker exec -it sagefy_postgres_1 pg_dump -U sagefy -a sagefy -p 2600 > "sagefy-$today.sql"
ls -al
b2 authorize_account $B2_ACCOUNT $B2_KEY
b2 sync /var/sagefy/dbbu b2:sagefy-dbbu
