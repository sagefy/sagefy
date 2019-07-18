FROM keymetrics/pm2:10-alpine
ADD . /client
WORKDIR /client
CMD ["pm2-runtime", "index.js"]
