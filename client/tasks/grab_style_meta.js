const glob = require('glob')
const fs = require('fs')
const yaml = require('js-yaml')

const build = (g, fn) => {
  const data = {}
  glob(g)
    .on('match', path => {
      const contents = fs.readFileSync(path, 'utf-8')
      ;(contents.match(/---(?!---)((.|\n)*?)---/g) || [])
        .filter(el => /---/.test(el))
        .map(el => el.replace(/---/g, ''))
        .forEach(y => {
          y = yaml.load(y)
          data[y.title] = y
        })
    })
    .on('end', () => fn(data))
}

module.exports = build
