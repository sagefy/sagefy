{div, h1, a, i} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    card = data.learnCards?[data.routeArgs[1]]

    return div({className: 'spinner'}) unless card

    return div(
        {
            id: 'card-learn'
            className: 'col-10'
        }

        kind(card)

        a(
            {className: 'continue button button--accent'}
            'Continue '
            i({className: 'fa fa-chevron-right'})
        )
    )

kind = (card) ->
    if card.kind is 'video'
        return require('./card_learn_video.tmpl')(card)
    if card.kind is 'choice'
        return require('./card_learn_choice.tmpl')(card)
