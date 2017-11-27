const grabStyleMeta = require('./grab_style_meta')
const fs = require('fs')

grabStyleMeta('./**/*.styl', (data) => {
  const content = JSON.stringify(data)
  fs.writeFile('./app/views/pages/styleguide.data.json', content)
})
