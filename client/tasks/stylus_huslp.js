/* eslint-disable import/no-extraneous-dependencies, max-params, max-len */
const husl = require('husl')
const stylus = require('stylus')

module.exports = function plugin() {
  return function _(style) {
    style.define('huslp', (h, s, l, a) => {
      const [r, g, b] = husl.p.toRGB(h.val, s.val, l.val)
      a = a || 1
      return new stylus.nodes.RGBA(r * 255, g * 255, b * 255, a)
    })
  }
}
