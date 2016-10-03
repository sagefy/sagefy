const diff = require('virtual-dom/diff')
const patch = require('virtual-dom/patch')
const createElement = require('virtual-dom/create-element')

const store = require('./store')
const broker = require('./broker')

module.exports = function (options) {
    const {view, el} = options

    let tree = view(store.data)
    let root = createElement(tree)
    el.appendChild(root)

    store.bind(function (data) {
        const next = view(data)
        root = patch(root, diff(tree, next))
        tree = next
    })

    broker.observe(el)
}
