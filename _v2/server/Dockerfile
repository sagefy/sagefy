FROM node:10.13-alpine
ADD . /server
WORKDIR /server
RUN npm install -g pm2
RUN npm install
CMD ["pm2", "start", "./index.js", "--no-daemon"]
