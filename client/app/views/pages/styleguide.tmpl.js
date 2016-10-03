// Note: we won't translate this copy as its dev specific
const {div, h1, h2, p} = require('../../modules/tags')

module.exports = () =>
    div(
        {id: 'styleguide'},
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
    const data = require('./styleguide.data.json')
    const tags = []
    Object.keys(data).forEach(title => {
        const o = data[title]
        o ? tags.push(
            h2(title),
            o.description ? p(o.description) : null
        ) : null
    })
    return tags
}

// TODO-2 render description markdown => vdom
// TODO-2 render example using .tmpl file
