FROM keymetrics/pm2:10-alpine
ADD . /server
WORKDIR /server
RUN npm install
CMD ["pm2-runtime", "index.js"]
