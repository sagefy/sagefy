FROM keymetrics/pm2:10-alpine
ADD . /client
WORKDIR /client
RUN npm install
CMD ["pm2-runtime", "start", "pm2.json"]
