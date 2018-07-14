FROM node:8.11.2-alpine
ADD . /client
WORKDIR /client
RUN echo -e 'http://dl-cdn.alpinelinux.org/alpine/edge/main\nhttp://dl-cdn.alpinelinux.org/alpine/edge/community\nhttp://dl-cdn.alpinelinux.org/alpine/edge/testing' > /etc/apk/repositories && \
  apk add --no-cache yarn
RUN yarn global add pm2
RUN yarn install
RUN yarn run build-server
CMD ["pm2", "start", "./server_dist/index.server.js", "--no-daemon"]
