const fs = require('fs')

const dist = 'distribution/'

const file = dist + 'index.html'
fs.readFile(file, 'utf8', (err, str) => {
    if(err) { throw new Error(err) }
    str = str.replace(/___/g, Date.now())
    fs.writeFile(file, str)
})
