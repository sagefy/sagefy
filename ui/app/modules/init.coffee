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
    for type in ['click', 'change', 'keydown', 'submit']
        @events[type] = {}
        el.addEventListener(type, @delegate(type))
