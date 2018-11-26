const express = require('express')

const app = express()

app.get('/', (req, res) => res.send('Sagefy V2 Client'))

app.get('/sitemap.txt', (req, res) => res.send('Do: https://sagefy.org'))

app.listen(process.env.PORT || 5984)
