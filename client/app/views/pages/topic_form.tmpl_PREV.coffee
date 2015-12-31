


module.exports = (data) ->


    return div(

        p(
            {className: 'leading'}
            strong(ucfirst(topicEntityKind))
            ": #{entityName}"
        )

    )
