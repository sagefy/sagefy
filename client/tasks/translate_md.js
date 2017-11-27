const fs = require('fs')

fs.readFile('./app/views/pages/terms.txt', 'utf8', (err, terms) => {
  let content = terms
    .split('\n\n')
    .map((t) => {
      if (t.indexOf('##') > -1) {
        return `${t.replace('## ', 'h2("')}")`
      }
      return `p("${t}")`
    })
    .map((s) => {
      return s.replace(/\n/g, ' ')
    })
    .join(',\n  ')
  content = `  ${content}`
  fs.writeFile(
    './app/views/pages/terms.content.js',
    `${"const {h2, p} = require('../../modules/tags')\n\n" +
      'module.exports = [\n'}${
      content
      }\n]\n`
  )
})
