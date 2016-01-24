{div, h1, a, i, p} = require('../../modules/tags')
spinner = require('../components/spinner.tmpl')
c = require('../../modules/content').get

module.exports = (data) ->
    id = data.routeArgs[0]
    card = data.learnCards?[id]

    return spinner() unless card

    pLearned = data.unitLearned?[card.unit_id]

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

    return [
        div(
            {
                id: 'card-learn'
                className: "#{card.kind} #{mode}"
                key: 'WbrGhHy5aUCmBVtHnlmTdJ1x'
            }

            kind(card, mode)

            p(
                {className: "card-learner__feedback--#{feedbackLabel}"}
                data.cardFeedback
            ) if data.cardFeedback

            p(
                a(
                    {
                        id: id
                        className: 'continue card-learner__continue'
                    }
                    'Continue '
                    i({className: 'fa fa-chevron-right'})
                )
            )
        )
        div(
            {
                key: '0Xe4fksADWwm9qWOMuTl7thD'
                className: 'card-learn__progress'
                style: {
                    width: pLearned * 100 + '%'
                }
            }
        ) if pLearned
    ]

kind = (card, mode) ->
    if card.kind is 'video'
        return require('./card_learn_video.tmpl')(card, mode)
    if card.kind is 'choice'
        return require('./card_learn_choice.tmpl')(card, mode)
