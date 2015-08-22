# Note: we won't translate this copy as its dev specific
{div, h1, p} = require('../../modules/tags')

module.exports = (data) ->
    return div(
        {id: 'styleguide', className: 'col-10'}
        h1(
            'Style Guide &amp; Component Library'
        )
        p(
            {className: 'leading'}
            '''
            Welcome to the Sagefy Style Guide. This page covers the styling and
            conventions of Sagefy user interfaces. This guide also include
            commonly used components. Suggestions are welcome via pull requests.
            '''
        )
        data.html
    )
