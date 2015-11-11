{div, h1, form, input, button, img,
 i, ul, li, strong, a, p, span} = require('../../modules/tags')
c = require('../../modules/content').get
{truncate, timeAgo} = require('../../modules/auxiliaries')

# TODO When search for entity's topic, show create topic button

module.exports = (data) ->
    loading = data.searchQuery and not data.searchResults

    return div(
        {id: 'search', className: 'col-8'}
        h1('Search')
        # TODO  add search filtering / ordering
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
                r[result._type + 'Result'](result)
            ) for result in data.searchResults
        ) if data.searchResults?.length
        p('No results found.') if data.searchResults?.length is 0
    )

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
        span(
            {className: 'time-ago'}
            timeAgo(result._source.created)
        )
    ]

r.postResult = (result) ->
    href = "/topics/#{result._source.topic_id}##{result._source.id}"
    return [
        strong('Post')
        ': '
        a(
            {href}
            truncate(result._source.body, 40)
        )
        ' by '
        a(
            {href: "/users/#{result._source.user_id}"}
        )
        # TODO topic name        result._source.topic_id ???
        # TODO entity kind       result._source.topic_id > ????
        # TODO entity name       result._source.topic_id > ????
        span(
            {className: 'time-ago'}
            timeAgo(result._source.created)
        )
    ]

r.cardResult = (result) ->
    return [
        strong('Card')
        ': '
        a(
            {href: "/cards/#{result._source.id}"}
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
            {href: "/units/#{result._source.id}"}
            result._source.name
        )
        ' – '
        truncate(result._source.body, 40)
    ]

r.setResult = (result) ->
    return [
        # TODO Add to my sets   (as learner)   result._source.id
        strong('Set')
        ': '
        a(
            {href: "/sets/#{result._source.id}"}
            result._source.name
        )
        ' – '
        truncate(result._source.body, 40)
        # TODO view units (as learner)   result._source.id
    ]
