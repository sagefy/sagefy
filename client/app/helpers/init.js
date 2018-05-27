/* eslint-disable global-require */
const snabbdom = require('snabbdom')
const patch = snabbdom.init([
  require('snabbdom/helpers/props').default,
  require('snabbdom/helpers/style').default,
  require('snabbdom/helpers/dataset').default,
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
