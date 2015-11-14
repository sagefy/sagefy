{div, h1, form, input, button, img,
 i, ul, li, strong, a, p, span} = require('../../modules/tags')
c = require('../../modules/content').get
{truncate, timeAgo, ucfirst} = require('../../modules/auxiliaries')

module.exports = (data) ->
    loading = data.searchQuery and not data.searchResults
    asLearner = data.route.indexOf('as_learner') > -1

    return div(
        {id: 'search', className: 'col-8'}
        h1('Search')
        # TODO add search filtering / ordering
        form(
            {className: 'form--horizontal'}
            div(
                {className: 'form-field form-field--search'}
                input({
                    type: 'search'
                    placeholder: 'Search'
                    name: 'search'
                    size: 40
                })
            )
            button(
                {type: 'submit'}
                i({className: 'fa fa-search'})
                ' Search'
            )
        )
        div({className: 'spinner'}) if loading
        ul(
            li(
                r[result._type + 'Result'](result, asLearner)
            ) for result in data.searchResults
        ) if data.searchResults?.length
        p('No results found.') if data.searchResults?.length is 0
    )

    # TODO pagination

r = {}

r.userResult = (result) ->
    return [
        strong('User')
        ': '
        a(
            {href: "/users/#{result._source.id}"}
            img({className: 'avatar', src: result._source.avatar})
            ' '
            result._source.name
        )
    ]

r.topicResult = (result) ->
    return [
        span(
            {className: 'timeago'}
            timeAgo(result._source.created)
        )
        strong('Topic')
        ': '
        a(
            {href: "/topics/#{result._source.id}"}
            result._source.name
        )
        ', '
        a(
            {href: "/#{result._source.entity.kind}/#{result._source.entity.id}"}
            result._source.entity.name
        )
        # TODO no of posts     ???
    ]

r.postResult = (result) ->
    href = "/topics/#{result._source.topic_id}##{result._source.id}"
    return [
        span(
            {className: 'timeago'}
            timeAgo(result._source.created)
        )
        strong(ucfirst(result._source.kind))
        ': '
        a(
            {href}
            truncate(result._source.body, 40)
        )
        ' by '
        a(
            {href: "/users/#{result._source.user.id}"}
            result._source.user.name
        )
        ' in topic: '
        a(
            {href: "/topics/#{result._source.topic.id}"}
            result._source.topic.name
        )
        # TODO entity kind       result._source.topic_id > ????
        # TODO entity name       result._source.topic_id > ????
    ]

r.cardResult = (result) ->
    return [
        strong('Card')
        ': '
        a(
            {href: "/cards/#{result._source.entity_id}"}
            result._source.name
        )
        # TODO unit name   result._source.unit_id > ???
        # TODO contents    ???
    ]

r.unitResult = (result) ->
    return [
        strong('Unit')
        ': '
        a(
            {href: "/units/#{result._source.entity_id}"}
            result._source.name
        )
        ' – '
        truncate(result._source.body, 40)
    ]

r.setResult = (result, asLearner = false) ->
    return [
        a(  # TODO if already in sets, don't show this button
            {
                id: result._source.entity_id
                href: '#'
                className: 'add-to-my-sets'
            }
            'Add to My Sets'
        ) if asLearner
        strong('Set')
        ': '
        a(
            {href: "/sets/#{result._source.entity_id}"}
            result._source.name
        )
        ' – '
        truncate(result._source.body, 40)
        ' ' if asLearner
        a(
            {href: "/sets/#{result._source.id}/tree", className: 'view-units'}
            'View Units'
        ) if asLearner
    ]
