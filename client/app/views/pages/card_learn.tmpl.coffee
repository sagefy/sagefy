{div, h1, a, i, p} = require('../../modules/tags')
c = require('../../modules/content').get

module.exports = (data) ->
    id = data.routeArgs[0]
    card = data.learnCards?[id]

    return div({className: 'spinner'}) unless card

    mode = if card.kind is 'video'
        'next-please'
    else if card.kind is 'choice'
        if data.cardResponse
            'next-please'
        else
            'answer'

    feedbackLabel = if data.cardResponse
        if data.cardResponse.score is 1
            'good'
        else
            'bad'
    else
        'accent'

    return div(
        {
            id: 'card-learn'
            className: "#{card.kind} col-8 #{mode}"
        }

        kind(card, mode)

        p(
            {className: "label--#{feedbackLabel}"}
            data.cardFeedback
        ) if data.cardFeedback

        p(
            {className: 'continue-wrap'}
            a(
                {
                    id: id
                    className: 'continue button button--accent'
                }
                'Continue '
                i({className: 'fa fa-chevron-right'})
            )
        )
    )

kind = (card, mode) ->
    if card.kind is 'video'
        return require('./card_learn_video.tmpl')(card, mode)
    if card.kind is 'choice'
        return require('./card_learn_choice.tmpl')(card, mode)
