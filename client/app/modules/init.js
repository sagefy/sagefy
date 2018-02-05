/* eslint-disable global-require */
const snabbdom = require('snabbdom')
const patch = snabbdom.init([
  require('snabbdom/modules/props').default,
  require('snabbdom/modules/style').default,
  require('snabbdom/modules/dataset').default,
])
const toVNode = require('snabbdom/tovnode').default

const store = require('./store')
const { getState } = require('./store')
const broker = require('./broker')

module.exports = function init({ view, el }) {
  broker.observe(el.parentNode)
  let tree = view(getState())
  patch(toVNode(el), tree)
  store.bind(data => {
    const next = view(data)
    patch(tree, next)
    tree = next
  })
}
