FROM node:6.11-alpine
ADD . /www
WORKDIR /www
RUN npm install pm2 -g
RUN npm install
CMD ["pm2", "start", "./app/index.server.js", "--no-daemon"]
