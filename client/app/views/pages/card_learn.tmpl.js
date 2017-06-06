const { div, a, p } = require('../../modules/tags')
const { isNumber } = require('../../modules/utilities')
const spinner = require('../components/spinner.tmpl')
// const c = require('../../modules/content').get
const icon = require('../components/icon.tmpl')

const kindTmpl = {}
kindTmpl.video = require('./card_learn_video.tmpl')
kindTmpl.choice = require('./card_learn_choice.tmpl')

module.exports = (data) => {
    const id = data.routeArgs[0]
    const card = data.learnCards && data.learnCards[id]

    if(!card) { return spinner() }

    const pLearned = data.unitLearned && data.unitLearned[card.unit_id]

    let mode
    if (card.kind === 'video') {
        mode = 'next-please'
    } else if (card.kind === 'choice') {
        if (isNumber(data.cardResponse.score)) {
            mode = 'next-please'
        } else {
            mode = 'answer'
        }
    }

    let feedbackLabel
    if (isNumber(data.cardResponse.score)) {
        if (data.cardResponse.score === 1) {
            feedbackLabel = 'good'
        } else {
            feedbackLabel = 'bad'
        }
    } else {
        feedbackLabel = 'accent'
    }

    return [
        div(
            {
                id: 'card-learn',
                className: `page ${card.kind} ${mode}`,
                key: 'WbrGhHy5aUCmBVtHnlmTdJ1x',
            },

            kind(card, mode),

            data.cardFeedback ? p(
                { className: `card-learner__feedback--${feedbackLabel}` },
                icon(feedbackLabel),
                ' ',
                data.cardFeedback
            ) : null,

            p(
                a(
                    {
                        id,
                        className: 'continue card-learner__continue',
                    },
                    'Continue ',
                    icon('next')
                )
            )
        ),
        pLearned ? div(
            {
                key: '0Xe4fksADWwm9qWOMuTl7thD',
                className: 'card-learn__progress',
                style: {
                    width: `${pLearned * 100}%`,
                },
            }
        ) : null,
    ]
}

const kind = (card, mode) => {
    if (card.kind === 'video') {
        return kindTmpl.video(card, mode)
    }
    if (card.kind === 'choice') {
        return kindTmpl.choice(card, mode)
    }
}
