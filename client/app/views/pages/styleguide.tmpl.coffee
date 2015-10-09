# Note: we won't translate this copy as its dev specific
{div, h1, h2, p, pre} = require('../../modules/tags')

module.exports = ->
    return div(
        {id: 'styleguide', className: 'col-10'}
        h1(
            'Style Guide & Component Library'
        )
        p(
            {className: 'leading'}
            '''
            Welcome to the Sagefy Style Guide. This page covers the styling and
            conventions of Sagefy user interfaces. This guide also include
            commonly used components. Suggestions are welcome via pull requests.
            '''
        )
        writeStyleguide()
    )

writeStyleguide = ->
    {outline} = require('./styleguide.outline.json')
    data = require('./styleguide.data.json')

    tags = []
    for title in outline
        o = data[title]
        tags.push(
            h2(o.title)
            p(o.description) if o.description
            pre(o.example) if o.example
        )

    return tags

# TODO render description markdown -> vdom
# TODO render example using .tmpl file instead of html examples
