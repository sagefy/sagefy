/* eslint-disable no-underscore-dangle */
const {div, h1, form, input, button, img,
 ul, li, strong, a, p} = require('../../modules/tags')
// const c = require('../../modules/content').get
const spinner = require('../components/spinner.tmpl')
// TP@ const timeago = require('../components/timeago.tmpl')
const icon = require('../components/icon.tmpl')
const previewSetHead = require('../components/preview_set_head.tmpl')
const previewUnitHead = require('../components/preview_unit_head.tmpl')
const previewCardHead = require('../components/preview_card_head.tmpl')

// TODO-2 when receiving ?kind={kind}, then search using that as well.

module.exports = (data) => {
    const loading = data.searchQuery && !data.searchResults
    const asLearner = data.route.indexOf('as_learner') > -1

    const inputOpts = {
        type: 'text',
        placeholder: 'Search',
        name: 'search',
        size: 40
    }

    inputOpts.value = data.searchQuery || null

    return div(
        {id: 'search', className: 'page'},
        h1('Search'),
        // TODO-2 add search filtering / ordering
        form(
            {className: 'form--horizontal'},
            div(
                {className: 'form-field form-field--search'},
                input(inputOpts)
            ),
            button(
                {type: 'submit'},
                icon('search'),
                ' Search'
            )
        ),
        loading ? spinner() : null,
        data.searchResults && data.searchResults.length ? ul(
            data.searchResults.map(result => li(
                r[result._type + 'Result'](result, asLearner)
            ))
        ) : null,
        data.searchResults && data.searchResults.length === 0 ?
            p('No results found.') :
            null
    )

    // TODO-2 pagination
}

const r = {}

r.userResult = (result) =>
    [
        strong(icon('user'), ' User'),
        ': ',
        a(
            {href: `/users/${result._source.id}`},
            img({className: 'avatar', src: result._source.avatar}),
            ' ',
            result._source.name
        )
    ]

r.topicResult = (/* TP@ result */) =>
    []
    /* TP@ [
        timeago(result._source.created, {right: true}),
        strong(icon('topic'), ' Topic'),
        ': ',
        a(
            {href: `/topics/${result._source.id}`},
            result._source.name
        ),
        ', ',
        a(
            {
                href:
                    `/${result._source.entity.kind}/${result._source.entity.id}`
            },
            result._source.entity.name
        )
        // TODO-2 no of posts     ???
    ] */

r.postResult = (/* TP@ result */) => {
    return []
    /* TP@
    const href = `/topics/${result._source.topic_id}#${result._source.id}`
    return [
        timeago(result._source.created, {right: true}),
        strong(icon('post'), ' ', ucfirst(result._source.kind)),
        ': ',
        a(
            {href},
            truncate(result._source.body, 40)
        ),
        ' by ',
        a(
            {href: `/users/${result._source.user.id}`},
            result._source.user.name
        ),
        ' in topic: ',
        result._source.topic ? a(
            {href: `/topics/${result._source.topic.id}`},
            result._source.topic.name
        ) : null
        // TODO-3 entity kind       result._source.topic_id > ????
        // TODO-3 entity name       result._source.topic_id > ????
    ] */
}

r.cardResult = (result) =>
    previewCardHead({
        url: `/cards/${result._source.entity_id}`,
        name: result._source.name,
        kind: result._source.kind,
        labelKind: true,
        // TODO-3 unit name   result._source.unit_id > ???
        // TODO-3 contents    ???
    })

r.unitResult = (result) =>
    previewUnitHead({
        url: `/units/${result._source.entity_id}`,
        name: result._source.name,
        body: result._source.body,
        labelKind: true,
    })

r.setResult = (result, asLearner = false) =>
    [
        asLearner ? a(  // TODO-2 if already in sets, don't show this button
            {
                id: result._source.entity_id,
                href: '#',
                className: 'add-to-my-sets'
            },
            icon('create'),
            ' Add to My Sets'
        ) : null,

        previewSetHead({
            url: `/sets/${result._source.entity_id}`,
            name: result._source.name,
            body: result._source.body,
            labelKind: true,
        }),
        asLearner ? ' ' : null,
        asLearner ? a(
            {
                href: `/sets/${result._source.entity_id}/tree`,
                className: 'view-units',
            },
            icon('unit'),
            ' View Units'
        ) : null
    ]
