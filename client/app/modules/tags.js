const h = require('virtual-dom/h')

const names = [
    // Super elements
    'meta',

    // Block-level layout elements
    'article', 'nav', 'aside', 'section', 'header', 'footer',

    // Other block-level elements
    'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'main', 'address',
    'p', 'hr', 'pre', 'blockquote', 'ol', 'ul', 'li', 'dl', 'dt', 'dd',
    'figure', 'figcaption', 'div', 'br', 'hgroup',

    // Table elements
    'table', 'caption', 'thead', 'tbody', 'tfoot',
    'tr', 'th', 'td', 'col', 'colgroup',

    // Form elements
    'form', 'fieldset', 'legend', 'label', 'input', 'button', 'select',
    'datalist', 'optgroup', 'option', 'textarea', 'output',
    'progress', 'meter',

    // Media elements
    'img', 'iframe', 'embed', 'object', 'param', 'video', 'audio', 'source',
    'canvas', 'track',

    //Inline elements
    'a', 'em', 'strong', 'i', 'small', 'abbr', 'del', 'ins',
    'q', 'cite', 'dfn', 'sub', 'sup', 'time', 'code', 'kbd', 'samp', 'var',
    'mark', 'span'
]

const tags = {}
const objConstructor = {}.constructor
names.forEach((name) =>
    tags[name] = (...args) => {
        if (args.length === 0) {
            return h(name)
        }
        if (args[0] && args[0].constructor === objConstructor) {
            return h(name, args[0], args.slice(1))
        }
        return h(name, args)
    }
)

module.exports = tags
