FROM keymetrics/pm2:12-alpine
ADD . /client
WORKDIR /client
CMD ["pm2-runtime", "index.js"]
