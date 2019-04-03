FROM postgres:11-alpine

RUN apk add postgresql-contrib
RUN apk add git
RUN apk add make
RUN git clone https://github.com/gavinwahl/postgres-json-schema.git && \
  cd postgres-json-schema && \
  make install
