{div, h1, form, input, button,
 i, ul, li, strong, a} = require('../../modules/tags')
c = require('../../modules/content').get
{truncate} = require('../../modules/auxiliaries')

# TODO When search for entity's topic, show create topic button
# TODO When `as_learner`, add the 'add to my sets' button

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
        ) if data.searchResults
        # TODO no results found message
    )

r = {}

r.userResult = (result) ->
    return [
        strong('User')
        ': '
        a(
            {href: "/users/#{result._source.id}"}
            result._source.name
        )
        # TODO avatar
    ]

r.topicResult = (result) ->
    return [
        strong('Topic')
        ': '
        a(
            {href: "/topics/#{result._source.id}"}
            result._source.name
        )
        # TODO entity name     result._source.entity ???
        # TODO entity kind     result._source.entity kind
        # TODO no of posts     ???
        # TODO time ago        result._source.created
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
        # TODO username/profile   result._source.user_id
        # TODO topic name        result._source.topic_id ???
        # TODO entity kind       result._source.topic_id > ????
        # TODO entity name       result._source.topic_id > ????
        # TODO time ago          result._source.created
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
        # TODO body         result._source.body
    ]

r.setResult = (result) ->
    return [
        strong('Set')
        ': '
        a(
            {href: "/sets/#{result._source.id}"}
            result._source.name
        )
        # TODO body         result._source.body
        # TODO Add to my sets / view units (as learner)   result._source.id
    ]
