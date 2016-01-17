# Note: we won't translate this copy as its dev specific
{div, h1, h2, p, pre} = require('../../modules/tags')

module.exports = ->
    return div(
        {id: 'styleguide'}
        h1(
            'Style Guide & Component Library'
        )
        p(
            '''
            Welcome to the Sagefy Style Guide. This page covers the styling and
            conventions of Sagefy user interfaces. This guide also include
            commonly used components. Suggestions are welcome via pull requests.
            '''
        )
        writeStyleguide()
    )

writeStyleguide = ->
    data = require('./styleguide.data.json')

    tags = []
    for title of data
        o = data[title]
        tags.push(
            h2(title)
            p(o.description) if o.description
        ) if o

    return tags

# TODO-2 render description markdown -> vdom
# TODO-2 render example using .tmpl file
