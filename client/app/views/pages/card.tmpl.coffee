{div, h1} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    return div({className: 'spinner'}) unless data.card

    return div(
        {id: 'card', className: 'col-10'}
        h1('Card')
    )

    # TODO@ show create topic button

    # Follow button
    # Flag button
    # Entity name
    # Entity kind and subkind
    # Language
    # Tags
    # Contents
        # Card - unique
        # Unit body
        # Set body, members
    # Stats section
        # Card - num learner, quality, diffulcty, guess, slip
        # Unit - num learner, quality, difficulty
        # Set - num learner, quality, difficulty
    # Relationships (Card, Unit only)
        # Belongs to, requires, required by
    # Topics
        # Name, posts, timeAgo
        # See more
    # Versions
        # Name, status, timeAgo
        # See More
