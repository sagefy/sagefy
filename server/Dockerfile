FROM keymetrics/pm2:12-alpine
ADD . /server
WORKDIR /server
CMD ["pm2-runtime", "index.js"]
