const snakeCase = require('lodash.snakecase')
const capitalize = require('lodash.capitalize')

module.exports = function titleize(str = '') { // Turns underscore or camel into title case
  return snakeCase(str)
    .split('_')
    .map(capitalize)
    .join(' ')
}
