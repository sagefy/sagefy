FROM node:6.11-alpine
ADD . /www
WORKDIR /www
RUN echo -e 'http://dl-cdn.alpinelinux.org/alpine/edge/main\nhttp://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/testing' > /etc/apk/repositories && \
  apk add --no-cache yarn
RUN yarn global add pm2
RUN yarn install
CMD ["pm2", "start", "./app/index.server.js", "--no-daemon"]
