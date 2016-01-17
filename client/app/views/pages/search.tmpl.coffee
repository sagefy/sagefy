{div, h1, form, input, button, img,
 i, ul, li, strong, a, p, span} = require('../../modules/tags')
c = require('../../modules/content').get
{truncate, ucfirst} = require('../../modules/auxiliaries')
spinner = require('../components/spinner.tmpl')
timeago = require('../components/timeago.tmpl')

# TODO-2 when receiving ?kind={kind}, then search using that as well.

module.exports = (data) ->
    loading = data.searchQuery and not data.searchResults
    asLearner = data.route.indexOf('as_learner') > -1

    inputOpts = {
        type: 'search'
        placeholder: 'Search'
        name: 'search'
        size: 40
    }

    inputOpts.value = data.searchQuery if data.searchQuery

    return div(
        {id: 'search'}
        h1('Search')
        # TODO-2 add search filtering / ordering
        form(
            {className: 'form--horizontal'}
            div(
                {className: 'form-field form-field--search'}
                input(inputOpts)
            )
            button(
                {type: 'submit'}
                i({className: 'fa fa-search'})
                ' Search'
            )
        )
        spinner() if loading
        ul(
            li(
                r[result._type + 'Result'](result, asLearner)
            ) for result in data.searchResults
        ) if data.searchResults?.length
        p('No results found.') if data.searchResults?.length is 0
    )

    # TODO-2 pagination

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
        timeago(result._source.created, {right: true})
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
        # TODO-2 no of posts     ???
    ]

r.postResult = (result) ->
    href = "/topics/#{result._source.topic_id}##{result._source.id}"
    return [
        timeago(result._source.created, {right: true})
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
        ) if result._source.topic
        # TODO-3 entity kind       result._source.topic_id > ????
        # TODO-3 entity name       result._source.topic_id > ????
    ]

r.cardResult = (result) ->
    return [
        strong('Card')
        ': '
        a(
            {href: "/cards/#{result._source.entity_id}"}
            result._source.name
        )
        # TODO-3 unit name   result._source.unit_id > ???
        # TODO-3 contents    ???
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
        a(  # TODO-2 if already in sets, don't show this button
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
            {
                href: "/sets/#{result._source.entity_id}/tree"
                className: 'view-units'
            }
            'View Units'
        ) if asLearner
    ]
