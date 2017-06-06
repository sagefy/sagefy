const h = require('virtual-dom/virtual-hyperscript/svg')

// https://developer.mozilla.org/en-US/docs/Web/SVG/Element
const names = [
    'svg', 'circle', 'line', 'text',
]

const tags = {}
const objConstructor = {}.constructor
names.forEach((name) => {
    tags[name] = (...args) => {
        if (args.length === 0) {
            return h(name)
        }
        if (args[0] && args[0].constructor === objConstructor) {
            return h(name, args[0], args.slice(1))
        }
        return h(name, args)
    }
})

module.exports = tags
