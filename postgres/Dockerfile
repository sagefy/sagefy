FROM postgres:11-alpine

ADD . /www
WORKDIR /www

RUN apk add postgresql-contrib

RUN apk add curl
RUN curl -fsSL -o /usr/local/bin/dbmate \
  https://github.com/amacneil/dbmate/releases/download/v1.4.1/dbmate-linux-musl-amd64
RUN chmod +x /usr/local/bin/dbmate

RUN apk add git
RUN apk add make
RUN git clone https://github.com/gavinwahl/postgres-json-schema.git && \
  cd postgres-json-schema && \
  make install
RUN git clone https://github.com/michelp/pgjwt.git && \
  cd pgjwt && \
  make install

# RUN dbmate -d "./migrations" -s "./schema.sql" up

CMD ["postgres"]

# docker-compose run postgres dbmate -d "./migrations" new "hello"
# docker-compose run postgres dbmate -d "./migrations" -s "./schema.sql" up
# docker-compose run postgres dbmate drop
