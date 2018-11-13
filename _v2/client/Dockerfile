FROM node:10.13-alpine
ADD . /client
WORKDIR /client
RUN npm install -g pm2
RUN npm install
CMD ["pm2", "start", "./index.server.js", "--no-daemon"]
