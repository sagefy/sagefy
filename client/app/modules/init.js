/* eslint-disable prefer-arrow-callback */
const diff = require('virtual-dom/diff')
const patch = require('virtual-dom/patch')
const createElement = require('virtual-dom/create-element')
const virtualize = require('vdom-virtualize')

const store = require('./store')
const broker = require('./broker')

module.exports = function init(options) {
    const {view, el} = options

    let tree
    let root

    if(el.innerHTML) {
        tree = virtualize(el)
        root = el.children[0]
    } else {
        tree = view(store.data)
        root = createElement(tree)
        el.innerHTML = ''
        el.appendChild(root)
    }

    store.bind(function update(data) {
        const next = view(data)
        root = patch(root, diff(tree, next))
        tree = next
    })

    broker.observe(el)
}
