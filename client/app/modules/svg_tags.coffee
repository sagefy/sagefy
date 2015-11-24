h = require('virtual-dom/virtual-hyperscript/svg')

# https://developer.mozilla.org/en-US/docs/Web/SVG/Element
names = [
    'svg', 'defs', 'circle', 'marker', 'path', 'line', 'text', 'rect'
]

tags = {}
objConstructor = {}.constructor
names.forEach((name) ->
    tags[name] = (args...) ->
        if args.length is 0
            return h(name)
        if args[0] and args[0].constructor is objConstructor
            return h(name, args[0], args.slice(1))
        return h(name, args)
)

module.exports = tags
