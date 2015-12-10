{div, h1, a, i} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    id = data.routeArgs[0]
    card = data.learnCards?[id]

    return div({className: 'spinner'}) unless card

    return div(
        {
            id: 'card-learn'
            className: "card-learn-#{card.kind} col-10"
        }

        kind(card)

        a(
            {
                id: id
                className: 'continue button button--accent'
            }
            'Continue '
            i({className: 'fa fa-chevron-right'})
        )
    )

kind = (card) ->
    if card.kind is 'video'
        return require('./card_learn_video.tmpl')(card)
    if card.kind is 'choice'
        return require('./card_learn_choice.tmpl')(card)
