const { iframe } = require('../../modules/tags')

module.exports = data =>
  iframe({
    className: 'unscored_embed',
    src: data.data.url,
    width: 13 * 58,
    height: 13 * 58 * 9 / 16,
    allowfullscreen: true,
  })
