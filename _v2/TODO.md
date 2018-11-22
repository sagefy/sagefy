- [ ] Create GraphQL query files
- [ ] Write GraphQL query files
- [ ] Configure DB & mail for dev, test, ci, prod
- [ ] Populate dev / text / CI dbs
- [ ] Write a new learner math simulation script
- [ ] Create a script to send mail
- [ ] Determine server/client error handling pattern
- [ ] Create sitemap route in client: root pages, card unit subject topic user


```json

  "scripts": {
    "start": "concurrently -p \"[{name}]\" --names watch-server,watch-client-node,watch-client-static  \"yarn run watch-server\" \"yarn run watch-client-node\" \"yarn run watch-client-static\"",
    "test": "exit 0",
    "watch-client-node": "chokidar 'client/**/*.{js,styl}' -c 'docker-compose restart client'",
    "watch-client-static": "cd client && yarn install && yarn start",
    "watch-server": "chokidar 'server/**/*.py' -c 'docker-compose restart server'"
  },
  "dependencies": {
    "concurrently": "3.5.0",
    "chokidar-cli": "1.2.0"
  }







  "scripts": {
    "build-scripts":
      "webpack ./app/index.js ../nginx/statics/index.js",
    "build-styles":
      "stylus --include-css --use hsluv-stylus --include ./app/ ./app/index.styl -o ../nginx/statics/index.css",


    "compress-scripts":
      "yarn run build-scripts && uglifyjs --compress --mangle --output ../nginx/statics/index.js -- ../nginx/statics/index.js",
    "compress-styles":
      "yarn run build-styles && cleancss ../nginx/statics/index.css -o ../nginx/statics/index.css",
    "deploy":
      "concurrently -p \"[{name}]\" --names compress-styles,compress-scripts \"yarn run compress-styles\" \"yarn run compress-scripts\"",


    "run-server": "node ./app/index.server.js",
    "run-tests": "jest",
    "start":
      "concurrently -p \"[{name}]\" --names watch-styles,watch-scripts \"yarn run watch-styles\" \"yarn run watch-scripts\"",


    "watch-scripts":
      "webpack --watch ./app/index.js ../nginx/statics/index.js -v",
    "watch-styles":
      "stylus --include-css --use hsluv-stylus --include ./app/ -w ./app/index.styl -o ../nginx/statics/index.css"
  },
  "jest": {
    "collectCoverage": true,
    "collectCoverageFrom": ["app/**/*.js"]
  },
  "dependencies": {
    "cookie-parser": "1.4.3",
    "express": "4.14.0",
    "query-string": "6.1.0",
  },
  "devDependencies": {
    "babel": "6.5.2",
    "babel-core": "6.5.2",
    "babel-loader": "6.2.7",
    "babel-preset-es2015": "6.16.0",
    "clean-css": "3.4.20",
    "glob": "5.0.15",
    "jest": "22.1.4",
    "json-loader": "0.5.4",
    "raw-loader": "0.5.1",
    "uglify-js": "3.4.0",
    "webpack": "1.13.3",
  }
}

```
