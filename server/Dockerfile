FROM keymetrics/pm2:10-alpine
ADD . /server
WORKDIR /server
CMD ["pm2-runtime", "index.js"]
