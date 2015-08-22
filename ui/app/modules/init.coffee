diff = require('virtual-dom/diff')
patch = require('virtual-dom/patch')
createElement = require('virtual-dom/create-element')

store = require('./store')
broker = require('./broker')
require('./route_actions')

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

    broker.el = el
    for type in Object.keys(broker.events)
        el.addEventListener(type, broker.delegate(type))
