diff = require('virtual-dom/diff')
patch = require('virtual-dom/patch')
createElement = require('virtual-dom/create-element')

store = require('./store')
broker = require('./broker')

module.exports = (options) ->
    {view, el} = options

    tree = view(store.data)
    root = createElement(tree)
    el.appendChild(root)

    store.bind((data) ->
        next = view(data)
        root = patch(root, diff(tree, next))
        tree = next
    )

    broker.observe(el)
