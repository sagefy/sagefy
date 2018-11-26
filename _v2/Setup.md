docker exec -it v2_postgres_1_4560933fd113 psql -U sagefy -a -v ON_ERROR_STOP=1 -f /www/sagefy.sql 
