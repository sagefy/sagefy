// Note: we won't translate this copy as its dev specific
const { div, h1, h2, p } = require('../../modules/tags')
const data = require('./styleguide.data.json')

module.exports = () =>
    div(
        { id: 'styleguide', className: 'page' },
        h1(
            'Style Guide & Component Library'
        ),
        p(
            'Welcome to the Sagefy Style Guide. ',
            'This page covers the styling and ',
            'conventions of Sagefy user interfaces. ',
            'This guide also include commonly used components. ',
            'Suggestions are welcome via pull requests. '
        ),
        writeStyleguide()
    )

const writeStyleguide = () => {
    const tags = []
    Object.keys(data).forEach((title) => {
        const o = data[title]
        if(o) {
            tags.push(
                h2(title),
                o.description ? p(o.description) : null
            )
        }
    })
    return tags
}

// TODO-2 render description markdown => vdom
// TODO-2 render example using .tmpl file
